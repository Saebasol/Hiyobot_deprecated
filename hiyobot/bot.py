from glob import glob
from os import getenv
from typing import Optional

import discord
from discord.ext.commands.bot import Bot

from utils.request import Request
from utils.mintchoco import HeliotropeResolver


class Hiyobot(Bot):
    def __init__(self, command_prefix, **options) -> None:
        super().__init__(
            command_prefix,
            help_command=None,
            description=None,
            **options,
        )
        self.heliotrope_issue = False
        self.maintenance = False
        self.maintenance_message = ""

        self.notion_secret = getenv("NOTION_SECRET")
        self.notion_database_id = getenv("NOTION_ID")
        self.mintchoco = HeliotropeResolver(getenv("HIYOBOT"))
        self.request: Optional[Request] = None


def load_cogs(bot: Hiyobot):
    extensions = list(
        map(
            lambda path: path.replace("./", "")
            .replace(".py", "")
            .replace("\\", ".")
            .replace("/", "."),
            filter(lambda path: "__" not in path, glob("./hiyobot/cogs/*/*")),
        )
    )
    extensions.append("jishaku")
    failed_list = []

    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)
            failed_list.append(extension)

    return failed_list


def run(token: str):
    intents = discord.Intents.default()
    bot = Hiyobot(command_prefix="설마프리픽스겹치겠냐", intents=intents)
    load_cogs(bot)
    bot.run(token)
