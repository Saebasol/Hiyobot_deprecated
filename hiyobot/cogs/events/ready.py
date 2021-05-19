import discord
from discord.ext import commands

import hiyobot
from hiyobot.bot import Hiyobot


class Ready(commands.Cog):
    def __init__(self, bot: Hiyobot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Login.. : ")
        print(self.bot.user.name)
        print(self.bot.user.id)

        game = discord.Game(f"&도움말 | {hiyobot.__version__}")
        await self.bot.change_presence(status=discord.Status.online, activity=game)


def setup(bot: Hiyobot):
    bot.add_cog(Ready(bot))
