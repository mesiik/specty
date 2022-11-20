from __future__ import annotations
from typing import Optional, Union, Dict
from discord import Message, Guild, User, Member, Embed
from discord.ext import commands


class Context(commands.Context):
    message: Message
    guild: Optional[Guild]
    author: Union[Member, User]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sent_messages: Dict[int] = {}

    @property
    def color(self) -> int:
        return 0xB4A7D6

    def process_message(self, message: Message) -> Message:
        self.sent_messages.update({self.message.id: message})
        return message

    async def ok(self, *args, **kwargs) -> Message:
        if "reference" not in kwargs:
            kwargs["reference"] = self.message.to_reference(fail_if_not_exists=False)

        if not kwargs.get("embed") and not kwargs.get("content") and args:
            embed = Embed()
            fmt = f"✅ {args[0]}"
            embed.color = 0xDEDEDE
            embed.description = fmt
            kwargs["embed"] = embed
            args = ()

        message = await super().send(*args, **kwargs)
        return self.process_message(message)

    async def error(self, *args, **kwargs) -> Message:
        if "reference" not in kwargs:
            kwargs["reference"] = self.message.to_reference(fail_if_not_exists=False)

        if not kwargs.get("embed") and not kwargs.get("content") and args:
            embed = Embed()
            fmt = f"⚠️ {args[0]}"
            embed.color = 0xFFD966
            embed.description = fmt
            kwargs["embed"] = embed
            args = ()

        message = await super().send(*args, **kwargs)
        return self.process_message(message)

    async def add_prefix(self, prefix: str) -> None:
        prefixes = self.bot.prefixes.get(self.guild.id)
        if prefixes is None:
            self.bot.prefixes[self.guild.id] = [prefix]
        else:
            self.bot.prefixes[self.guild.id].append(prefix)
        await self.bot.pool.execute(
            "INSERT INTO prefixes(guild_id, prefix) VALUES($1, $2)",
            self.guild.id,
            prefix,
        )

    async def remove_prefix(self, prefix: str) -> None:
        prefixes = self.bot.prefixes.get(self.guild.id)
        if prefixes:
            self.bot.prefixes[self.guild.id].remove(prefix)
        await self.bot.pool.execute(
            "DELETE FROM prefixes WHERE guild_id = $1 AND prefix = $2",
            self.guild.id,
            prefix,
        )
