import aiocache
import discord
from discord.ext import commands

from utils.pagenator import pagenator


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cache = aiocache.Cache()

    @commands.command(name="도움말", aliases=["help", "도움", "commands", "명령어"])
    async def _help(self, ctx):
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

        await self.cache.set("help_embed", embed_list)
        await pagenator(self.bot, ctx, msg, self.cache, "help_embed")


def setup(bot):
    bot.add_cog(Help(bot))
