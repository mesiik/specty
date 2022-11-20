from specty.cogs.bot.base import Command
from specty.vault76.command import group
from specty.vault76.context import Context
from discord.ext.commands import has_guild_permissions
from discord import Message, Embed


class PrefixCommand(Command):
    @group(name="prefix", aliases=["prefixes"], invoke_without_command=True)
    async def _prefix(self, ctx: Context) -> Message:
        """
        Returns server prefixes.
        """
        prefixes = []
        prefixes.append(ctx.me.mention)
        _extra = ctx.bot.prefixes.get(ctx.guild.id)
        if _extra:
            prefixes.extend(_extra)
        embed = Embed(color=ctx.color)
        embed.set_author(
            name=ctx.author.display_name, icon_url=ctx.author.display_avatar
        )
        embed.description = "\n".join(f"{prefixes.index(i)+1}. {i}" for i in prefixes)
        return await ctx.ok(embed=embed)

    @_prefix.command(name="add")
    @has_guild_permissions(manage_guild=True)
    async def _prefix_add(self, ctx: Context, prefix: str) -> Message:
        if prefix in self.bot.prefixes.get(ctx.guild.id):
            return await ctx.ok("prefix already added.")
        await ctx.add_prefix(prefix)
        return await ctx.ok("added prefix.")

    @_prefix.command(name="remove")
    @has_guild_permissions(manage_guild=True)
    async def _prefix_remove(self, ctx: Context, prefix: str) -> Message:
        if prefix in self.bot.prefixes.get(ctx.guild.id):
            await ctx.remove_prefix(prefix)
            return await ctx.ok("removed prefix.")
        return await ctx.error("prefix not found.")
