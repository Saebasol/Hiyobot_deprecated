from __future__ import annotations

from typing import Literal, get_args

BASE_URL = "https://nekos.life/api/"
VERSION = "v2"

URL = BASE_URL + VERSION

# dummy ["v3","nekoapi_v3.1"]

nsfw_tags_literal = Literal[
    "Random_hentai_gif",
    "cum_jpg",
    "futanari",
    "femdom",
    "smallboobs",
    "anal",
    "nsfw_neko_gif",
    "pussy_jpg",
    "nsfw_avatar",
    "boobs",
    "blowjob",
    "hentai",
    "tits",
    "erok",
    "feetg",
    "bj",
    "erokemo",
    "kuni",
    "les",
    "trap",
    "hololewd",
    "lewdk",
    "solog",
    "pussy",
    "yuri",
    "lewdkemo",
    "lewd",
    "pwankg",
    "eron",
    "keta",
    "eroyuri",
    "holoero",
    "classic",
    "feet",
    "gasm",
    "spank",
    "erofeet",
    "ero",
    "solo",
    "cum",
]

sfw_tags_literal = Literal[
    "tickle",
    "ngif",
    "meow",
    "poke",
    "kiss",
    "8ball",
    "lizard",
    "slap",
    "cuddle",
    "goose",
    "avatar",
    "fox_girl",
    "hug",
    "gecg",
    "pat",
    "smug",
    "kemonomimi",
    "holo",
    "wallpaper",
    "woof",
    "baka",
    "feed",
    "neko",
    "waifu",
]

sfw_tags = get_args(sfw_tags_literal)
nsfw_tags = get_args(nsfw_tags_literal)
