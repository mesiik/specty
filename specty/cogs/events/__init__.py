from specty.vault76.module import Module
from typing import TYPE_CHECKING
from discord import Forbidden, HTTPException, NotFound
from discord.ext.commands import (
    CommandNotFound,
    MissingPermissions,
    NSFWChannelRequired,
    DisabledCommand,
    NotOwner,
    CommandOnCooldown,
    NoPrivateMessage,
    ConversionError,
    BadArgument,
    ChannelNotReadable,
    MessageNotFound,
    RoleNotFound,
    GuildNotFound,
    BadInviteArgument,
    BadColorArgument,
    PartialEmojiConversionFailure,
    EmojiNotFound,
    UserInputError,
    BotMissingPermissions,
    CheckFailure,
    ObjectNotFound,
    BadBoolArgument,
    CommandInvokeError,
    Paginator,
    UserNotFound,
    MemberNotFound,
    ChannelNotFound,
    NotOwner,
)

if TYPE_CHECKING:
    from specty.vault76.bot import SpectralCore


class Events(Module):
    def __init__(self, bot: "SpectralCore"):
        self.bot = bot

    @Module.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, "on_error"):
            return

        elif isinstance(error, CommandNotFound):
            return

        elif isinstance(error, Forbidden):
            return await ctx.error(error)

        elif isinstance(error, NSFWChannelRequired):
            return

        elif isinstance(error, MissingPermissions):
            perms = [f"`{p}`" for p in error.missing_permissions]
            return await ctx.error(
                f"You don't have {', '.join(perms).replace('_', '.')} permission(s)"
            )

        elif isinstance(error, BotMissingPermissions):
            perms = [f"`{p}`" for p in error.missing_permissions]
            return await ctx.error(
                f"I'am missing {', '.join(perms).replace('_', '.')} permissions(s)"
            )

        elif isinstance(error, DisabledCommand):
            return await ctx.error(f"This command is disabled")

        elif isinstance(error, NotOwner):
            return

        elif isinstance(error, CommandOnCooldown):
            await ctx.warn(f"you are on cooldown, try after `{error.retry_after:.2f}s`")

        elif isinstance(error, NoPrivateMessage):
            return

        elif isinstance(error, HTTPException):
            return await ctx.error(str(error))

        elif isinstance(error, CheckFailure):
            return

        elif isinstance(error, NotFound):
            return await ctx.error(
                "provided asset/user was not found, that might be discord skill issue."
            )

        elif isinstance(error, ConversionError):
            return await ctx.error("Provided argument is not valid.")

        if isinstance(error, BadArgument):
            ctx.command.reset_cooldown(ctx)
            if isinstance(error, UserNotFound):
                await ctx.error(f"User not found.")
            elif isinstance(error, MemberNotFound):
                await ctx.error(f"Member not found.")
            elif isinstance(error, ChannelNotFound):
                await ctx.error(f"Channel not found.")
            elif isinstance(error, ChannelNotReadable):
                await ctx.error(
                    f"I don't have permissions to read messages in {error.argument.mention}."
                )
            elif isinstance(error, MessageNotFound):
                await ctx.error(f"Message not found.")
            elif isinstance(error, RoleNotFound):
                await ctx.error(f"Role not found.")
            elif isinstance(error, GuildNotFound):
                await ctx.error(f"Guild not found.")
            elif isinstance(error, BadInviteArgument):
                await ctx.error(f"Invite not found.")
            elif isinstance(
                error,
                (EmojiNotFound, PartialEmojiConversionFailure),
            ):
                await ctx.error(f"Invalid emoji.")
            elif isinstance(error, ObjectNotFound):
                await ctx.error(f"Invalid identificator.")
            elif isinstance(error, BadBoolArgument):
                await ctx.error(f"Not valid boolean option.")
            elif isinstance(error, BadColorArgument):
                await ctx.error(f"Invalid color.")
            else:
                helper = (
                    str(ctx.invoked_subcommand)
                    if ctx.invoked_subcommand
                    else str(ctx.command)
                )
                return await ctx.send_help(helper)

        elif isinstance(error, UserInputError):

            helper = (
                str(ctx.invoked_subcommand)
                if ctx.invoked_subcommand
                else str(ctx.command)
            )
            return await ctx.send_help(helper)

        elif isinstance(error, CheckFailure):
            return
        else:
            if isinstance(error, CommandInvokeError):
                original = error.original
                if "Forbidden" in str(original) or "HTTPException" in str(original):
                    return await ctx.reply(error.original)
                return await ctx.error(original)


async def setup(bot: "SpectralCore") -> None:
    await bot.add_cog(Events(bot))
