import discord
from discord.ext import commands

import Hiyobot
from Hiyobot.bot import Hiyobot as class_hiyobot


class Ready(commands.Cog):
    def __init__(self, bot: class_hiyobot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Login.. : ")
        print(self.bot.user.name)
        print(self.bot.user.id)

        game = discord.Game(f"&도움말 | {Hiyobot.__version__}")
        await self.bot.change_presence(status=discord.Status.online, activity=game)


def setup(bot: class_hiyobot):
    bot.add_cog(Ready(bot))
