import time
import aiocache
import discord
from rose.client import _Client


def parse_value_url(value_url_list: list):
    if not value_url_list:
        return ["없음"]
    else:
        return [
            f"[{value_url_dict['value']}](https://hitomi.la{value_url_dict.url})"
            for value_url_dict in value_url_list
        ]


def make_embed_with_info(info: dict):
    tags_join = ",".join(parse_value_url(info.tags))
    embed = discord.Embed(
        title=info.title["value"],
        description=f"[{info.language['value']}]({info.language['url']})",
        url=info.title["url"],
    )
    embed.set_thumbnail(url=f"https://doujinshiman.ga/v2/api/proxy/{info.thumbnail}")
    embed.add_field(
        name="번호",
        value=f"[{info.galleryid}](https://hitomi.la/reader/{info.galleryid}.html)",
        inline=False,
    )
    embed.add_field(
        name="타입", value=f"[{info.type['value']}]({info.type['url']})", inline=False
    )
    embed.add_field(
        name="작가", value=",".join(parse_value_url(info.artist)), inline=False
    )
    embed.add_field(
        name="그룹", value=",".join(parse_value_url(info.group)), inline=False
    )
    embed.add_field(
        name="원작", value=",".join(parse_value_url(info.series)), inline=False
    )
    embed.add_field(
        name="캐릭터", value=",".join(parse_value_url(info.characters)), inline=False
    )
    embed.add_field(
        name="태그",
        value=tags_join if len(tags_join) <= 1024 else "표시하기에는 너무길어요",
        inline=False,
    )
    return embed


def make_embed_with_progress_info(progress: list):
    embed = discord.Embed(title="다운로드 정보입니다.")

    for info in progress:
        if not info.link:
            link = ""
        else:
            link = f"다운로드: [링크]({info.link})"

        embed.add_field(
            name=info.index,
            value=f"남은 횟수: {info.count}\n\n진행 상황: {info.task_status}\n\n{link}",
        )

    return embed


def make_viewer_embed(index: int, file_name: str, total, num):
    return (
        discord.Embed()
        .set_image(url=f"https://doujinshiman.ga/image/{index}/{file_name}")
        .set_footer(text=f"{total}쪽중 {num}쪽")
    )


class RoseExt(_Client):
    def __init__(self, authorization):
        super().__init__(authorization)
        self.cache = aiocache.Cache()

    async def cache_list_embed(self, number):
        lists = await self.list_(number)
        if lists.status != 200:
            return discord.Embed(title="정보를 찾을수 없습니다")
        embed = [make_embed_with_info(list_) for list_ in lists.list]
        await self.cache.set("list_embed", embed)

    async def info_embed(self, index):
        info = await self.info(index)
        if info.status != 200:
            return discord.Embed(title="정보를 찾을수 없습니다")
        return make_embed_with_info(info)

    async def cache_viewer_embed(self, index):
        galleryinfo = await self.galleryinfo(index)
        embed = []
        num = 0
        if galleryinfo.status != 200:
            return discord.Embed(title="정보를 찾을수 없습니다")
        await self.download(index)
        for file_info in galleryinfo.files:
            num += 1
            embed.append(
                make_viewer_embed(index, file_info.name, len(galleryinfo.files), num)
            )
        await self.cache.set("viewer_embed", embed)

    async def download_embed(self, user_id, index):
        galleryinfo = await self.galleryinfo(index)
        if galleryinfo.status != 200:
            return discord.Embed(title="정보를 찾을수 없습니다")
        else:
            response = await self.download(index, user_id, True)
            if response.status == 200:
                return discord.Embed(
                    title="성공적으로 요청했어요", description="``&현황``을 사용해서 다운로드 현황을 확인할수 있어요."
                )
            else:
                return discord.Embed(
                    title="가입되지 않은 유저 이거나 오류가 발생했어요",
                    description="``&가입``을 사용해서 가입할수있어요",
                )

    async def progress_embed(self, user_id):
        progress = await self.progress(user_id)
        if progress.status != 200:
            return discord.Embed(title="기록을 찾을수 없습니다")
        else:
            return make_embed_with_progress_info(progress.info)

    async def register_embed(self, user_id, check):
        response = await self.register(user_id, check)
        if check:
            if response.status == 200:
                return False
            elif response.status == 404:
                return True
        else:
            if response.status == 201:
                return discord.Embed(title="가입 되었습니다.")

    async def latency(self):
        heliotrope_latency1 = time.perf_counter()
        await self.request("GET", "/")
        heliotrope_latency2 = time.perf_counter()
        return heliotrope_latency2 - heliotrope_latency1