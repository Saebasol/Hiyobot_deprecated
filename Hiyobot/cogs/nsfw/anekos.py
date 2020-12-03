import random

import anekos
import discord
from discord.ext import commands


class Nekos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.neko_client = anekos.NekosLifeClient()

    @commands.command(name="네코", aliases=["neko"])
    async def _neko(self, ctx: commands.Context, tag: str = None):
        """
        귀여운 네코미미를 보여줍니다. 태그를 사용해서 검색도 가능합니다.

        사용할 수 있는 값 : 태그(선택)

        사용 예시 : ``&네코`` 또는 ``&네코 wallpaper``
        """
        embed = discord.Embed()

        SFW_tags = [x.name for x in list(anekos.SFWImageTags)]
        NSFW_tags = [x.name for x in list(anekos.NSFWImageTags)]

        SFW_random = [anekos.SFWImageTags.NEKO, anekos.SFWImageTags.NEKOGIF]
        NSFW_random = ["lewd", anekos.NSFWImageTags.NSFW_NEKO_GIF]

        if tag == "도움말":
            embed = discord.Embed(title="사용할 수 있는 태그 목록입니다.")
            embed.add_field(name="전연령 태그", value="\n".join(SFW_tags))
            embed.add_field(name="성인 태그", value="\n".join(NSFW_tags))
            return await ctx.send(embed=embed)

        if tag:
            upper_tag = tag.upper()
            if not ctx.channel.nsfw:
                if upper_tag in NSFW_tags:
                    return await ctx.send(
                        "해당 태그는 성인 태그인 것 같습니다. 연령 제한이 설정된 채널에서 사용해주세요."
                    )
                elif upper_tag in SFW_tags:
                    image = await self.neko_client.image(upper_tag.lower())
                else:
                    return await ctx.send("해당 태그는 없어요! 태그는 ``&네코 도움말``을 통해 확인하실 수 있어요.")
            else:
                if upper_tag in NSFW_tags or upper_tag in SFW_tags:
                    image = await self.neko_client.image(upper_tag.lower())
                else:
                    return await ctx.send("해당 태그는 없어요! 태그는 ``&네코 도움말``을 통해 확인하실 수 있어요.")
        else:
            image = await self.neko_client.image(
                random.choice(SFW_random if not ctx.channel.nsfw else NSFW_random)
            )

        embed.set_image(url=image.url)
        await ctx.send(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Nekos(bot))
