import os

import discord
import sentry_sdk
from discord.ext import commands

import Hiyobot


class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Login.. : ")
        print(self.bot.user.name)
        print(self.bot.user.id)

        game = discord.Game(f"&도움말 | {Hiyobot.__version__}")
        await self.bot.change_presence(status=discord.Status.online, activity=game)


def setup(bot):
    bot.add_cog(Ready(bot))
