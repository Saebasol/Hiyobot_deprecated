import os
import sys
import time
from json.decoder import JSONDecodeError

import discord
import humanize
import psutil
from aiohttp.client_exceptions import ContentTypeError
from discord.ext import commands

import Hiyobot
from utils.hiyobi import HiyobiExt
from utils.pixiv import PixivExt
from utils.rose_ext import RoseExt


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.proc = psutil.Process()
        self.hiyobi = HiyobiExt()
        self.rose = RoseExt(os.environ["heliotrope_auth"])
        self.pixiv = PixivExt()

    @commands.command(name="정보", aliases=["info"])
    async def _botinfo(self, ctx: commands.Context):
        """
        봇의 자세한 정보를 가져옵니다.

        사용 예시 : ``&정보``
        """
        message_latency1 = time.perf_counter()
        await ctx.trigger_typing()
        message_latency2 = time.perf_counter()

        try:
            hiyobi_latency = round(await self.hiyobi.latency() * 1000, 2)
        except JSONDecodeError:
            hiyobi_latency = None

        try:
            heliotrope_latency = round(await self.rose.latency() * 1000, 2)
        except ContentTypeError:
            heliotrope_latency = None

        try:
            pixiv_latency = round(await self.pixiv.latency() * 1000, 2)
        except ContentTypeError:
            pixiv_latency = None

        embed = discord.Embed(
            title=f"Info\nCommand prefix: `&`\nHiyobot: `{Hiyobot.__version__}`",
            description=f"Python `{sys.version}` on `{sys.platform}`".replace("\n", ""),
            url="https://saebasol.statuspage.io/",
        )
        embed.add_field(
            name="discord.py version", value=f"{discord.__version__}", inline=False
        )
        with self.proc.oneshot():

            mem = self.proc.memory_full_info()
            name = self.proc.name()
            pid = self.proc.pid
            thread_count = self.proc.num_threads()

            embed.add_field(
                name="Using physical memory", value=f"{humanize.naturalsize(mem.rss)}"
            )
            embed.add_field(
                name="Using virtual memory", value=f"{humanize.naturalsize(mem.vms)}"
            )
            embed.add_field(
                name="Which unique to this process",
                value=f"{humanize.naturalsize(mem.uss)}",
            )
            embed.add_field(name="PID", value=f"{pid}")
            embed.add_field(name="Process name", value=f"{name}")
            embed.add_field(name="Thread(s)", value=f"{thread_count}")
        embed.add_field(name="Guild(s)", value=f"{len(self.bot.guilds)}")
        embed.add_field(name="User(s)", value=f"{len(self.bot.users)}")
        embed.add_field(
            name="Average websocket latency",
            value=f"{round(self.bot.latency * 1000, 2)}ms",
        )
        embed.add_field(
            name="Average message latency",
            value=f"{round((message_latency2 - message_latency1) * 1000, 2)}ms",
            inline=False,
        )
        embed.add_field(
            name="Average Hiyobi API server latency",
            value=f"{hiyobi_latency if hiyobi_latency else '가져올 수 없음'}ms",
        )
        embed.add_field(
            name="Average Heliotrope server latency",
            value=f"{heliotrope_latency if heliotrope_latency else '가져올 수 없음'}ms",
        )
        embed.add_field(
            name="Average Pixiv API server latency",
            value=f"{pixiv_latency if pixiv_latency else '가져올 수 없음'}ms",
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))
