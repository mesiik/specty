import logging
import sys

__all__ = ("setup",)


def setup() -> None:
    log = logging.getLogger()
    logging.getLogger("aiohttp").setLevel(logging.DEBUG)
    logging.getLogger("discord").setLevel(logging.DEBUG)
    logging.getLogger("discord.http").setLevel(logging.DEBUG)
    logging.getLogger("discord.state").setLevel(logging.DEBUG)
    log.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    fmt = logging.Formatter(
        "\033[31m|specty.{module:<10}| \033[0m |\033[35m{levelname:<8}\033[0m|  |\033[34m{threadName}\033[37m:\033[30m{process}\033[0m|  |\033[35m{asctime}\033[0m|   {message}",
        "%Y-%m-%d %H:%M:%S",
        style="{",
    )
    console_handler.setFormatter(fmt)
    log.addHandler(console_handler)
