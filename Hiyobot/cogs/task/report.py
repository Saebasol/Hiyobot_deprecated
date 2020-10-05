import datetime
import os

import aiohttp
from discord.ext import commands, tasks

from utils.rose_ext import RoseExt


class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.environ["status_api_key"]
        self.page_id = os.environ["page_id"]
        self.metric_id = os.environ["metric_id"]
        self.rose = RoseExt(os.environ["heliotrope_auth"])
        self.report.start()

    @tasks.loop(minutes=5.0)
    async def report(self):
        headers = {
            "Content-Type": "application/json",
            "Authorization": "OAuth " + self.api_key,
        }
        heliotrope_latency = round(await self.rose.latency() * 1000, 2)
        time_stamp = datetime.datetime.now().timestamp()
        param = {
            "data": {
                self.metric_id: [{"timestamp": time_stamp, "value": heliotrope_latency}]
            }
        }
        async with aiohttp.ClientSession() as cs:
            async with cs.post(
                f"https://api.statuspage.io/v1/pages/{self.page_id}/metrics/data",
                headers=headers,
                json=param,
            ) as r:
                response = await r.json()
                print(response)

    @report.before_loop
    async def before_report(self):
        print("waiting...")
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Report(bot))
