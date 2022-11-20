from specty.cogs.config.prefix import PrefixCommand
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from specty.vault76.bot import SpectralCore


class Config(PrefixCommand):
    def __init__(self, bot: "SpectralCore"):
        self.bot = bot


async def setup(bot: "SpectralCore") -> None:
    await bot.add_cog(Config(bot))
