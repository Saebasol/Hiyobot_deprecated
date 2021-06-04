import discord
from discord.ext.commands.cog import Cog

import hiyobot
from hiyobot.bot import Hiyobot
from utils.request import Request


class Ready(Cog):
    def __init__(self, bot: Hiyobot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Login.. : ")
        print(self.bot.user.name)
        print(self.bot.user.id)

        game = discord.Game(f"&도움말 | {hiyobot.__version__}")
        await self.bot.change_presence(status=discord.Status.online, activity=game)
        self.bot.request = Request()


def setup(bot: Hiyobot):
    bot.add_cog(Ready(bot))
