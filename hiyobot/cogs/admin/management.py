from discord.embeds import Embed
from discord.ext.commands.cog import Cog
from discord.ext.commands.context import Context
from discord.ext.commands.core import command, is_owner
from discord.ext.tasks import loop

from hiyobot.bot import Hiyobot


class Management(Cog):
    def __init__(self, bot: Hiyobot):
        self.bot = bot
        self.check_heliotrope.start()

    @loop(minutes=5.0)
    async def check_heliotrope(self):
        try:
            await self.bot.rose.latency()  # will changed
        except:
            self.bot.heliotrope_issue = True
        else:
            self.bot.heliotrope_issue = False

    async def bot_check(self, ctx: Context):
        if self.bot.maintenance and not await self.bot.is_owner(ctx.author):
            await ctx.send(
                embed=Embed(
                    title="봇이 점검중입니다.",
                    description=f"사유: ``{self.bot.maintenance_message}``\n\n[공식 디코](https://discord.gg/PSshFYr)",
                )
            )
            return False
        else:
            if self.bot.maintenance:
                await ctx.send("경고: 유지보수 상태입니다.")

        return True

    @command("상태")
    @is_owner()
    async def _setting(self, ctx: Context):
        if self.bot.heliotrope_issue or self.bot.maintenance:
            maintenance_embed = Embed(title="In progress issue")

            if self.bot.heliotrope_issue:
                maintenance_embed.add_field(
                    name="Heliotrope issue", value=str(self.bot.heliotrope_issue)
                )

            if self.bot.maintenance:
                maintenance_embed.add_field(
                    name="Maintenance status", value=str(self.bot.maintenance)
                )
                maintenance_embed.add_field(
                    name="Maintenance message", value=self.bot.maintenance_message
                )
        else:
            maintenance_embed = Embed(title="Everything OK :)")

        await ctx.send(embed=maintenance_embed)

    @command("서버이슈")
    @is_owner()
    async def _make_heliotrope_issue(self, ctx: Context):
        if self.bot.heliotrope_issue:
            self.bot.heliotrope_issue = False
            await ctx.send(
                f"Successfully close heliotrope_issue: {self.bot.heliotrope_issue}"
            )
        else:
            self.bot.heliotrope_issue = True
            await ctx.send(
                f"Successfully open heliotrope_issue: {self.bot.heliotrope_issue}"
            )

    @command("유지보수")
    @is_owner()
    async def _maintenance(self, ctx: Context, *message: str):
        if self.bot.maintenance:
            self.bot.maintenance = False
            self.bot.maintenance_message = ""
            await ctx.send(
                f"Successfully stop under maintenance: {self.bot.maintenance}"
            )
        else:
            if not message:
                return await ctx.send("Need purpose")
            self.bot.maintenance = True
            self.bot.maintenance_message = " ".join(message)
            await ctx.send(
                f"Successfully start under maintenance: {self.bot.maintenance}"
            )


def setup(bot: Hiyobot):
    bot.add_cog(Management(bot))
