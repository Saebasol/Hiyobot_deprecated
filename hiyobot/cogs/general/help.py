import discord
from discord.ext import commands
from discord.ext.commands.context import Context

from hiyobot.bot import Hiyobot
from utils.pagenator import pagenator


class Help(commands.Cog):
    def __init__(self, bot: Hiyobot):
        self.bot = bot

    @commands.command(name="도움말", aliases=["help", "도움", "commands", "명령어"])
    async def _help(self, ctx: Context):
        msg = await ctx.send(embed=discord.Embed(title="도움말을 만들고 있어요"))
        command_list = [
            i for i in self.bot.commands if i.help if "jishaku" not in i.name
        ]

        embed_list = []

        for command in command_list:
            embed = discord.Embed(
                title="도움말", description=f"접두사: ``{self.bot.command_prefix}``"
            )

            embed.add_field(
                name=command.name,
                value=command.help,
                inline=False,
            )
            embed.set_footer(text="공식디코: https://discord.gg/PSshFYr")

            embed_list.append(embed)

        await pagenator(self.bot, ctx, msg, embed_list)


def setup(bot: Hiyobot):
    bot.add_cog(Help(bot))
