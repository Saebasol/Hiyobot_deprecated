import asyncio
import sys
import time
from json.decoder import JSONDecodeError

import discord
import humanize
import psutil
from aiohttp.client_exceptions import ContentTypeError
from discord.ext import commands

import hiyobot
from hiyobot.bot import Hiyobot


class Info(commands.Cog):
    def __init__(self, bot: Hiyobot):
        self.bot = bot
        self.proc = psutil.Process()

    @commands.command(name="정보", aliases=["info"])
    async def _botinfo(self, ctx: commands.Context):
        """
        봇의 자세한 정보를 가져옵니다.

        사용 예시 : ``&정보``
        """
        message_latency = time.perf_counter()
        await ctx.trigger_typing()
        latency = round((time.perf_counter() - message_latency) * 1000, 2)

        hiyobi_latency = self.bot.hiyobi.latency()
        heliotrope_latency = self.bot.rose.latency()
        pixiv_latency = self.bot.pixiv.latency()

        await asyncio.wait([hiyobi_latency, heliotrope_latency, pixiv_latency])

        try:
            hiyobi_latency = round(hiyobi_latency * 1000, 2)
        except JSONDecodeError:
            hiyobi_latency = None

        try:
            heliotrope_latency = round(heliotrope_latency * 1000, 2)
        except ContentTypeError:
            heliotrope_latency = None

        try:
            pixiv_latency = round(pixiv_latency * 1000, 2)
        except ContentTypeError:
            pixiv_latency = None

        embed = discord.Embed(
            title=f"Info\nCommand prefix: `&`\nHiyobot: `{hiyobot.__version__}`",
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
        embed.add_field(
            name="Average websocket latency",
            value=f"{round(self.bot.latency * 1000, 2)}ms",
            inline=False,
        )
        embed.add_field(
            name="Average message latency",
            value=f"{latency}ms",
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


def setup(bot: Hiyobot):
    bot.add_cog(Info(bot))
