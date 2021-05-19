from glob import glob

import discord
from discord.ext.commands import Bot


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


def load_cogs(bot: Hiyobot):
    extensions = list(
        map(
            lambda path: path.replace("./", "")
            .replace(".py", "")
            .replace("\\", ".")
            .replace("/", "."),
            filter(lambda path: "__" not in path, glob("./Hiyobot/cogs/*/*")),
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
    bot.run(token)
