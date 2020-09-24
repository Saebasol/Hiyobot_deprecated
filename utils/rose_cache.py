import aiocache
import discord
from rose.client import _Client


def parse_value_url(value_url_list: list):
    if not value_url_list:
        return ["없음"]
    else:
        return [f"[{value_url_dict['value']}](https://hitomi.la{value_url_dict.url})" for value_url_dict in value_url_list]

def make_embed_with_info(info:dict):
    embed = discord.Embed(
        title=info.title["value"],
        description=f"[{info.language['value']}]({info.language['url']})",
        url=info.title["url"],
    )
    embed.add_field(name="번호", value=info.galleryid)
    embed.add_field(name="타입", value=f"[{info.type['value']}]({info.type['url']})")
    embed.add_field(name="직가", value=",".join(parse_value_url(info.artist)))
    embed.add_field(name="그룹", value=",".join(parse_value_url(info.group)))
    embed.add_field(name="원작", value=",".join(parse_value_url(info.series)))
    embed.add_field(name="캐릭터", value=",".join(parse_value_url(info.characters)))
    embed.add_field(name="태그", value=",".join(parse_value_url(info.tags)))
    return embed


class RoseCache(_Client):
    def __init__(self, authorization):
        super().__init__(authorization)
        self.cache = aiocache.Cache()

    async def cahe_list_embed(self, number):
        lists = self.list_(number)
        pass
