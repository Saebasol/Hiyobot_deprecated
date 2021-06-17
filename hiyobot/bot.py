from glob import glob
from os import getenv
from typing import Optional
import hiyobot
import discord
from discord.ext.commands.bot import Bot

from utils.mintchoco import HeliotropeResolver
from utils.pixiv import PixivResolver
from utils.request import Request
import sentry_sdk


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
        self.pixiv = PixivResolver()
        self.request: Optional[Request] = None

    async def on_error(self, event_method, *args, **kwargs):
        raise


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
    bot = Hiyobot(command_prefix="&", intents=intents)
    load_cogs(bot)
    sentry_sdk.init(getenv("SENTRY_DSN"), release=hiyobot.__version__)
    bot.run(token)
