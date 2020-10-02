import os
import sys
import time

import discord
import humanize
import psutil
from discord.ext import commands

import Hiyobot

from utils.hiyobi import HiyobiExt
from utils.rose_ext import RoseExt


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.proc = psutil.Process()
        self.hiyobi = HiyobiExt()
        self.rose = RoseExt("")

    @commands.command(name="정보", aliases=["info"])
    async def _botinfo(self, ctx):

        message_latency1 = time.perf_counter()
        await ctx.trigger_typing()
        message_latency2 = time.perf_counter()

        hiyobi_latency = await self.hiyobi.latency()

        heliotrope_latency = await self.rose.latency()

        embed = discord.Embed(
            title=f"Info\nCommand prefix: `&`\nHiyobot: `{Hiyobot.__version__}`",
            description=f"Python `{sys.version}` on `{sys.platform}`".replace("\n", ""),
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
            inline=False,
        )
        embed.add_field(
            name="Average message latency",
            value=f"{round((message_latency2 - message_latency1) * 1000, 2)}ms",
        )
        embed.add_field(
            name="Average Hiyobi API server latency",
            value=f"{round(hiyobi_latency * 1000, 2)}ms",
        )
        embed.add_field(
            name="Average Heliotrope server latency",
            value=f"{round(heliotrope_latency * 1000, 2)}ms",
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Info(bot))