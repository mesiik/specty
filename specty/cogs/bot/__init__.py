from specty.cogs.bot.ping import PingCommand
from specty.cogs.bot.botinfo import BotinfoCommand
from specty.cogs.bot.lastfm import LastfmCommand
from specty.cogs.bot.eval import EvalCommand
from typing import TYPE_CHECKING
from discord.ext.commands import DefaultHelpCommand, Group
from discord import Embed

if TYPE_CHECKING:
    from specty.vault76.bot import SpectralCore

__all__ = ("Command",)


class Help(DefaultHelpCommand):
    async def send_bot_help(self, _):
        ctx = self.context
        cogs = [c for c in ctx.bot.cogs.keys()]
        cog_objects = [ctx.bot.get_cog(c) for c in cogs]
        embed = Embed(color=ctx.color, title=f"{ctx.bot.user.name} help")
        embed.set_author(
            name=ctx.author.display_name, icon_url=ctx.author.display_avatar
        )
        for cog in cog_objects:
            if cog.qualified_name == "Jishaku":
                continue
            if hasattr(cog, "hidden"):
                if cog.hidden:
                    continue
            commands = cog.get_commands()
            if not commands == list():

                if hasattr(cog, "icon"):
                    name = f"{cog.icon} {cog.qualified_name}"
                else:
                    name = f"{cog.qualified_name}"

                embed.add_field(
                    name=name,
                    value=", ".join(
                        map(lambda command_name: f"`{command_name}`", commands)
                    ),
                    inline=False,
                )

        return await ctx.ok(embed=embed)

    def do_command(self, command):
        ctx = self.context
        embed = Embed()
        embed.color = ctx.color
        fmt = "command"
        is_group = False
        if isinstance(command, Group):
            fmt = "group"
            is_group = True
        embed.title = f"{fmt}: {command}"
        embed.description = command.help
        embed.add_field(
            name="Usage",
            value=f'```\n{command} {str(command.signature).replace("_", " ") if command.signature else " "}\n```',
            inline=False,
        )
        embed.add_field(
            name="Aliases",
            value=f'{", ".join(command.aliases) if command.aliases else "N/A"}',
            inline=False,
        )
        if command.cooldown is not None:
            embed.add_field(
                name="cooldown",
                value=f"{command.cooldown.rate}/{command.cooldown.per}s",
                inline=False,
            )
        if is_group:
            listed = "\n".join(f"{c.qualified_name}" for c in command.commands)
            embed.add_field(name="Options", value=f"```\n{listed}\n```")
        return embed

    async def send_group_help(self, group):
        return await self.context.ok(embed=self.do_command(group))

    async def send_command_help(self, command):
        await self.context.ok(embed=self.do_command(command))


class Bot(PingCommand, LastfmCommand, BotinfoCommand, EvalCommand):
    def __init__(self, bot: "SpectralCore"):
        self.bot = bot
        bot.help_command = Help()
        bot.help_command.cog = self


async def setup(bot: "SpectralCore") -> None:
    await bot.add_cog(Bot(bot))
