from specty.cogs.bot.base import Command
from specty.vault76.command import command
from specty.vault76.context import Context
from discord import Message


class PingCommand(Command):
    @command(name="ping", aliases=["latency"])
    async def _ping(self, ctx: Context) -> Message:
        """
        Returns bot latency
        """
        websocket, rest = await ctx.bot.ping()

        return await ctx.ok(f"Pong! ws: {websocket*1000:.2f}ms rest: {rest*1000:.2f}ms")
