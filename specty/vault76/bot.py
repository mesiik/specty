__all__ = ("SpectralCore",)

from discord.ext.commands import AutoShardedBot as AB
from os import environ
from typing import Tuple, Union, Dict
from specty.utils.logging import setup
from specty.utils import get_prefix
from specty.vault76.context import Context
from discord import Intents, AllowedMentions, MemberCacheFlags, http, Message
from datetime import timedelta, datetime
from dotenv import load_dotenv
import logging
import time
import jishaku
import asyncpg

setup()
load_dotenv()
environ["JISHAKU_NO_UNDERSCORE"] = "True"
environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
environ["JISHAKU_HIDE"] = "True"
environ["JISHAKU_FORCE_PAGINATOR"] = "True"
environ["JISHAKU_RETAIN"] = "True"


class SpectralCore(AB):
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            help_command=None,
            intents=Intents.all(),
            member_cache_flags=MemberCacheFlags(joined=True, voice=False),
            case_insensitive=True,
            strip_after_prefix=True,
            allowed_mentions=AllowedMentions.none(),
        )
        self.log = logging.getLogger(__name__)
        self.pool: asyncpg.Pool = None
        self.prefixes: Dict[int] = {}
        self.connection = datetime.now()

    async def setup_hook(self) -> None:
        self.pool = await asyncpg.connect(
            host=environ.get("POSTGRESQL_HOST"), 
            user=environ.get("POSTGRESQL_USER"), 
            password=environ.get("POSTGRESQL_PASSWORD")
        )
        self.log.info("Database connected")
        startup_extensions = [
            "jishaku",
            "specty.cogs.bot",
            "specty.cogs.events",
            "specty.cogs.config",
        ]
        await self.load_extensions(*startup_extensions)

    async def get_context(self, message, *, cls=Context):
        return await super().get_context(message, cls=cls)

    async def ping(self) -> Tuple[int]:
        start = time.perf_counter()
        ws = self.latency
        await self.http.request(http.Route("GET", "/users/@me"))
        end = time.perf_counter()
        return ws, end - start

    async def on_message(self, message: Message) -> None:
        if message.author.bot:
            return
        await self.process_commands(message)

    async def load_extensions(self, *extensions) -> None:
        for extension in extensions:
            await self.load_extension(extension)
            self.log.info(f"Loaded extension {extension}")

    async def on_connect(self) -> None:
        self.log.warning("Attempting to start")

    async def on_shard_ready(self, shard_id) -> None:
        self.log.info(f"Created shard #{shard_id}")

    async def on_ready(self) -> None:
        for guild in self.guilds:
            prefixes = await self.pool.fetch(
                "SELECT * FROM prefixes WHERE guild_id = $1", guild.id
            )
            self.prefixes[guild.id] = [data.get("prefix") for data in prefixes]
        self.log.info(f"logged in as {self.user} (ID: {self.user.id})")

    async def on_message_edit(self, before: Message, after: Message) -> None:
        if before.content == after.content:
            return

        if not after.edited_at:
            return

        if after.edited_at - after.created_at > timedelta(minutes=1):
            return

        await self.process_commands(after)

    async def async_run(self) -> None:
        await self.login(environ.get("DISCORD_TOKEN"))
        await self.connect()

    def get_message(self, message_id: int) -> Union[Message, None]:
        return self._connection._get_message(message_id)
