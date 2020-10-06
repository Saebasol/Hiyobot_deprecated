import logging

import discord
from discord.ext.commands import Bot

logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


def load_cogs(bot):
    extensions = [
        "jishaku",
        "events.error",
        "events.ready",
        "general.help",
        "general.patchnote",
        "general.info",
        "general.register",
        "nsfw.anekos",
        "nsfw.heliotrope",
        "nsfw.hiyobi",
        "task.report",
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


intents = discord.Intents.all()
bot = Bot(command_prefix="&", help_command=None, intents=intents)
