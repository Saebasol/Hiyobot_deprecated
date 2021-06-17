from asyncio.exceptions import TimeoutError
from contextlib import suppress
from typing import Any

from discord.embeds import Embed
from discord.ext.commands.cog import Cog
from discord.ext.commands.context import Context
from discord.ext.commands.core import command

from hiyobot.bot import Hiyobot
from utils.notion import Notion


class Contact(Cog):
    def __init__(self, bot: Hiyobot) -> None:
        self.bot = bot

    async def bug_or_enhancement(self, ctx: Context):
        msg = await ctx.send(
            embed=Embed(
                title="문의하실 형식을 선택해주세요",
                description="🐛 는 버그를 의미합니다.\n🚀는 건의 및 기능 요청을 의미합니다.\n❎는 취소입니다.\n"
                "작성 도중 취소 하실려면 '취소' 또는 'cancel'이라 작성하시면 취소됩니다.\n"
                "본인이 깃허브 계정이 있으시다면 [해당 레포](https://github.com/Saebasol/Hiyobot)에서 이슈를 직접 작성하실수있습니다."
                "\n\n[공식 디스코드](https://discord.gg/PSshFYr)",
            )
        )
        await msg.add_reaction("🐛")
        await msg.add_reaction("🚀")
        await msg.add_reaction("❎")
        try:
            reaction, user = await self.bot.wait_for(
                "reaction_add",
                check=lambda r, u: (u == ctx.author)
                and (r.emoji in ["🐛", "🚀", "❎"])
                and (r.message == msg),
                timeout=60.0,
            )
        except TimeoutError:
            return await msg.edit(embed=Embed(title="시간이 초과되었어요.")), "stop"

        if reaction.emoji == "🐛":
            return msg, True

        if reaction.emoji == "🚀":
            return msg, False

        return await msg.edit(embed=Embed(title="취소되었어요.")), "stop"

    @command("문의")
    async def _contact(self, ctx: Context):
        """
        개발자에게 직접 문의할수있습니다.

        사용 예시 ``&문의``
        """
        notion = Notion(self.bot.notion_database_id)
        steps: list[Any] = [notion.set_title]

        bug = [
            notion.set_step_to_reproduce,
            notion.set_expected_result,
            notion.set_actual_result,
        ]

        enhancement = [notion.set_description]

        mapping = {
            notion.set_title: Embed(title="제목을 입력해주세요"),
            notion.set_step_to_reproduce: Embed(
                title="재현할수있는 방법을 알려주세요", description="Shift + Enter를 눌러 줄바꿈을 사용하실수있어요"
            ),
            notion.set_expected_result: Embed(title="예상한 정상적인 동작은 무엇인가요?"),
            notion.set_actual_result: Embed(title="현재 무슨 동작이 일어나고있나요?"),
            notion.set_description: Embed(
                title="설명을 입력해주세요", description="Shift + Enter를 눌러 줄바꿈을 사용하실수있어요"
            ),
        }

        msg, bug_or_enhancement = await self.bug_or_enhancement(ctx)

        if bug_or_enhancement:
            if bug_or_enhancement == "stop":
                return
            notion.set_tags(True)
            steps.extend(bug)
        else:
            notion.set_tags(False)
            steps.extend(enhancement)

        with suppress(Exception):
            await msg.clear_reactions()

        for step in steps:
            await msg.edit(embed=mapping[step])

            try:
                message = await self.bot.wait_for(
                    "message",
                    check=lambda m: m.channel.id == ctx.channel.id
                    and m.author.id == ctx.author.id,
                    timeout=60.0,
                )
            except TimeoutError:
                return await msg.edit(embed=Embed(title="시간이 초과되었어요."))
            else:
                if message.content in ["취소", "cancel"]:
                    await message.delete()
                    return await msg.edit(embed=Embed(title="취소 되었어요."))

                step(message.content)
                with suppress(Exception):
                    await message.delete()

        notion.set_author(f"{ctx.author}({ctx.author.id})")

        r = await self.bot.request.post(
            "https://api.notion.com/v1/pages",
            "json",
            headers={"Authorization": self.bot.notion_secret},
            json=notion.to_dict(),
        )
        if r.status == 200:
            page_id = r.body["id"].replace("-", "")
            await msg.edit(
                embed=Embed(
                    title="정상적으로 요청되었어요",
                    description=f"[이곳에서 확인하실수있어요.](https://www.notion.so/{self.bot.notion_database_id}/{page_id})\n\n[공식 디스코드](https://discord.gg/PSshFYr)",
                )
            )
        else:
            await msg.edit(
                embed=Embed(
                    title="요청 실패.",
                    description=f"[공식 디스코드](https://discord.gg/PSshFYr)",
                )
            )


def setup(bot: Hiyobot):
    bot.add_cog(Contact(bot))
