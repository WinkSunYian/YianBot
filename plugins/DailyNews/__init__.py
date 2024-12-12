from nonebot import on_fullmatch
from nonebot.adapters.onebot.v11 import (
    MessageSegment,
    MessageEvent
)


news = on_fullmatch("#每日新闻", priority=5, block=True)


@news.handle()
async def help_handle(event: MessageEvent):
    url = "https://zj.v.api.aa1.cn/api/60s-v2/?cc=小逸安~"
    await news.finish(MessageSegment.image(url))
