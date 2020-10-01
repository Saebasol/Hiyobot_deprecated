import os
import discord
from discord.ext import commands

import Hiyobot
import sentry_sdk


class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # login,status
    @commands.Cog.listener()
    async def on_ready(self):
        sentry_sdk.init(
            dsn=os.environ["sentry"],
            release=f"hiyobot@{Hiyobot.__version__}",
        )

        # login
        print("Login.. : ")
        print(self.bot.user.name)
        print(self.bot.user.id)
        print("======================")
        print(f"{len(set(self.bot.get_all_members()))}명이 봇을 사용하고 있습니다..")
        print("======================")

        # Status
        game = discord.Game(f"&도움말 | {Hiyobot.__version__}")
        await self.bot.change_presence(status=discord.Status.online, activity=game)