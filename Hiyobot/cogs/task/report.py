import datetime
import os

import aiohttp
from discord.ext import commands, tasks

from utils.rose_ext import RoseExt


def make_incident(schedule, components_id):
    incident = {
        "incident": {
            "name": "string",
            "status": "investigating",
            "impact_override": "critical",
            "scheduled_for": schedule,
            "scheduled_until": schedule,
            "scheduled_remind_prior": True,
            "scheduled_auto_in_progress": True,
            "scheduled_auto_completed": True,
            "metadata": {},
            "deliver_notifications": True,
            "auto_transition_deliver_notifications_at_end": True,
            "auto_transition_deliver_notifications_at_start": True,
            "auto_transition_to_maintenance_state": True,
            "auto_transition_to_operational_state": True,
            "auto_tweet_at_beginning": True,
            "auto_tweet_on_completion": True,
            "auto_tweet_on_creation": True,
            "auto_tweet_one_hour_before": True,
            "backfill_date": "string",
            "backfilled": True,
            "body": "string",
            "components": {"component_id": "major_outage"},
            "component_ids": [components_id],
            "scheduled_auto_transition": True,
        }
    }

    return incident


class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.environ["status_api_key"]
        self.page_id = os.environ["page_id"]
        self.metric_id = os.environ["metric_id"]
        self.components_id = os.environ["components_id"]
        self.rose = RoseExt(os.environ["heliotrope_auth"])
        self.report.start()

    def stop_report(self):
        self.report.cancel()

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
                if r.status != 404:
                    async with cs.post(
                        f"https://api.statuspage.io/pages/{self.page._id}/incidents",
                        headers=headers,
                        json=make_incident(
                            datetime.datetime.now().isoformat(), self.components_id
                        ),
                    ) as r:
                        if r.status == 201:
                            response = await r.json()
                            print(response)
                            self.stop_report()

                response = await r.json()
                print(response)

    @report.before_loop
    async def before_report(self):
        print("waiting...")
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Report(bot))
