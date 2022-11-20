from specty.cogs.bot.base import Command
from specty.vault76.command import command
from specty.vault76.context import Context
from discord import Message, Embed


class BotinfoCommand(Command):
    @command(name="botinfo", aliases=["about", "bi", "bot"])
    async def _botinfo(self, ctx: Context) -> Message:
        """
        Returns bot latency
        """
        embed = Embed(color=ctx.color)
        embed.set_author(
            name=ctx.author.display_name, icon_url=ctx.author.display_avatar
        )
        embed.add_field(
            name=f"** **",
            value=f"**Guilds:** {len(ctx.bot.guilds)}\n**Users:** {len(ctx.bot.users)} (cache)\n**Uptime:** <t:{int(ctx.bot.connection.timestamp())}:R>",
        )
        return await ctx.ok(embed=embed)
