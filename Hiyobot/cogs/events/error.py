from discord.ext import commands

from Hiyobot.bot import Hiyobot


class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(
                "명령어를 찾을 수 없습니다. `&도움말` 명령어를 사용해 전체 명령어 목록을 볼 수 있습니다.", delete_after=5
            )

        elif isinstance(error, commands.NSFWChannelRequired):
            await ctx.send(
                "연령 제한(NSFW)이 설정된 채널에서만 사용하실 수 있습니다. 이 명령어를 사용하려면 채널 관리자가 `채널 설정 -> 연령 제한 채널`을 활성화해야 합니다.",
                delete_after=5,
            )

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                "명령어 사용법이 잘못되었습니다. 값이 부족합니다. `&도움말` 명령어를 통해 정확한 사용법을 보실 수 있습니다.",
                delete_after=5,
            )

        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                "명령어 사용법이 잘못되었습니다. 지정한 값이 잘못되었습니다. `&도움말` 명령어를 통해 정확한 사용법을 보실 수 있습니다.",
                delete_after=5,
            )


def setup(bot: Hiyobot):
    bot.add_cog(Error(bot))
