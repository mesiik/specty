from discord import Message
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from specty.vault76.bot import SpectralCore


async def get_prefix(bot: "SpectralCore", message: Message) -> List[str]:

    prefixes = [f"<@!{bot.user.id}>", f"<@{bot.user.id}>"]

    if not message.guild:
        return prefixes

    _extra = bot.prefixes.get(message.guild.id)
    if _extra:
        prefixes.extend(_extra)

    return prefixes
