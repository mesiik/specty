from specty.cogs.bot.base import Command
from specty.vault76.command import command
from specty.vault76.context import Context
from jishaku.codeblocks import codeblock_converter
from discord import Message, Embed
from discord.ext.commands import is_owner


class EvalCommand(Command):
    @command(name="eval")
    @is_owner()
    async def _eval(self, ctx: Context, *, code: codeblock_converter) -> Message:
        """
        no.
        """
        return await ctx.invoke(ctx.bot.get_command("jishaku python"), argument=code)
