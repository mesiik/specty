__all__ = ["Module"]

import asyncio
import logging
from typing import Callable, List, Any, TypeVar
import aiohttp
from discord.ext import commands

F = TypeVar("F", bound=Callable[..., Any])
C = commands.Cog


class Module(C):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot
        self.name = type(self).__name__.lower()
        self.log: logging.Logger = logging.getLogger(f"cog.{self.name}")
        self.session = aiohttp.ClientSession(loop=self.loop)
        self._scheduled_tasks: List[asyncio.Task[Any]] = []
        self._setup_schedules()
        self.disabled_in = []

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self.bot.loop

    @property
    def pool(self):
        return self.bot.pool

    def cog_unload(self) -> None:
        for scheduled_task in self._scheduled_tasks:
            self.log.debug("Cancelling scheduled task: %s", scheduled_task)
            scheduled_task.cancel()

        self.loop.create_task(self.session.close())
