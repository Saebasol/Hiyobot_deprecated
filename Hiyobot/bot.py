import logging
import os

import discord
from discord.ext.commands import Bot

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


def load_cogs(bot: Bot):
    extensions = [
        "jishaku",
        "events.error",
        "events.ready",
        "general.help",
        "general.patchnote",
        "general.info",
        "general.auth",
        "nsfw.anekos",
        "nsfw.heliotrope",
        "nsfw.hiyobi",
        "nsfw.pixiv",
    ]

    failed_list = []

    for extension in extensions:
        try:
            bot.load_extension(
                "Hiyobot.cogs." + extension if "." in extension else extension
            )
        except Exception as e:
            print(e)
            failed_list.append(extension)

    return failed_list


class Bot(Bot):
    def __init__(
        self, command_prefix, help_command=None, description=None, **options
    ) -> None:
        super().__init__(
            command_prefix,
            help_command=help_command,
            description=description,
            **options
        )
        self.github_token = os.environ.get("GitHub")
        self.verify = os.environ.get("VERIFY")


intents = discord.Intents.default()
bot = Bot(command_prefix="&", intents=intents)
