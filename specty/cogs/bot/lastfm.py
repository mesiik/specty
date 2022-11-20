from specty.cogs.bot.base import Command
from specty.vault76.command import group
from specty.vault76.context import Context
from typing import Optional
from discord import Message, Member, Embed, utils
from dotenv import load_dotenv
from os import environ
import aiohttp

load_dotenv()
BASE_URL = "http://ws.audioscrobbler.com/2.0/"


class LastfmCommand(Command):
    async def api_request(self, params: dict, ignore_errors=False):

        params["api_key"] = environ.get("LASTFM_KEY")
        params["format"] = "json"
        tries = 0
        max_tries = 2
        while True:
            async with aiohttp.ClientSession() as session:
                async with session.get(BASE_URL, params=params) as response:
                    try:
                        data = await response.json()
                    except aiohttp.client_exceptions.ContentTypeError:
                        if ignore_errors:
                            return None
                        text = await response.text()
                        raise Exception(text)

                    if data is None:
                        raise Exception(
                            "Could not connect to LastFM",
                        )
                    if response.status == 200 and data.get("error") is None:
                        return data
                    if int(data.get("error")) == 8:
                        tries += 1
                        if tries < max_tries:
                            continue

                    if ignore_errors:
                        return None
                    raise Exception(data.get("message"))

    @group(name="lastfm", aliases=["fm", "lfm"], invoke_without_command=True)
    async def lastfm(self, ctx: Context, member: Optional[Member]) -> Message:
        member = member or ctx.author
        _data = await self.bot.pool.fetchrow(
            "SELECT * FROM lastfm WHERE user_id = $1", member.id
        )
        if not _data:
            return await ctx.error("user has no last.fm account connected.")
        data = await self.api_request(
            {
                "user": _data.get("username"),
                "method": "user.getrecenttracks",
                "limit": 1,
            }
        )
        tracks = data["recenttracks"]["track"]

        if not tracks:
            return await ctx.error("no tracks found.")

        artist = tracks[0]["artist"]["#text"]
        track = tracks[0]["name"]
        image_url = tracks[0]["image"][-1]["#text"]
        embed = Embed(color=ctx.color)
        embed.set_thumbnail(url=image_url)
        embed.add_field(name="Track", value=f"{track}")
        embed.add_field(name="Artist", value=f"{artist}")
        trackdata = await self.api_request(
            {
                "user": _data.get("username"),
                "method": "track.getInfo",
                "artist": artist,
                "track": track,
            },
            ignore_errors=True,
        )
        userinfo = await self.api_request(
            {"user": _data.get("username"), "method": "user.getinfo"},
            ignore_errors=True,
        )
        if trackdata is not None:
            tags = []
            try:
                trackdata = trackdata["track"]
                playcount = int(trackdata["userplaycount"])
                if playcount > 0:
                    embed.description = f"\n> {playcount:,} plays • {int(userinfo['user']['playcount']):,} scrobbles"
                for tag in trackdata["toptags"]["tag"]:
                    tags.append(tag["name"])
                embed.set_footer(text=", ".join(tags))
            except (KeyError, TypeError) as e:
                print(e)

        embed.set_author(
            name=f"{_data.get('username')}",
            icon_url=member.display_avatar.url,
        )

        message = await ctx.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")
        return message

    @lastfm.command(name="set")
    async def lastfm_set(self, ctx: Context, username: str):
        data = await self.api_request(
            {"user": username, "method": "user.getinfo"}, ignore_errors=True
        )
        if data is None:
            return await ctx.error("this last.fm account is invalid")

        username = data["user"]["username"]

        _data = await self.bot.pool.fetchrow(
            "SELECT * FROM lastfm WHERE user_id = $1", ctx.author.id
        )
        if not _data:
            await self.bot.pool.execute(
                "INSERT INTO lastfm(user_id, username) VALUES($1, $2)",
                ctx.author.id,
                username,
            )
        else:
            await self.bot.pool.execute(
                "UPDATE lastfm SET username = $2 WHERE user_id = $1",
                ctx.author.id,
                username,
            )

        return await ctx.ok(f"logged in as <https://last.fm/user/{username}>")
