from specty.vault76.bot import SpectralCore
import asyncio


async def main() -> None:
    async with SpectralCore() as bot:
        try:
            await bot.async_run()
        except (KeyboardInterrupt, RuntimeError):
            exit(0)


if __name__ == "__main__":
    asyncio.run(main())
