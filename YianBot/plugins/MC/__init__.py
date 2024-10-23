import json
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
from random import randint, choice
import os

__plugin_name__ = "MC"
__plugin_usage__ = "我的世界"

mc = on_message(priority=10)


word = [
    "有人陪我玩生存租赁服吗\n服号:26526063",
    "有人玩生存租赁服吗,有雪球菜单\n服号:26526063",
    "有没有人陪我玩生存租赁服\n服号:26526063",
]
at_word = [
    "\n玩不玩生存租赁服,有雪球菜单\n服号:26526063",
    "\n能不能陪我一起玩生存租赁服\n服号:26526063",
    "\n生存租赁服玩吗\n服号:26526063",
]
tome_word = [
    "\n网易纯生存租赁服,目前续租了一年,有雪球菜单|随机传送|玩家互传\n服号:26526063",
    "\n你要玩这个生存租赁服吗",
    "\n服号:26526063,你玩了就知道了",
]

with open("./group.json", "r") as f:
    group_name_dict = json.load(f)
print(group_name_dict)


# 获取群名称
async def get_group_name(bot: Bot, group_id):
    group_id = str(group_id)
    if group_id in group_name_dict:
        return group_name_dict[group_id]
    else:
        group_info = await bot.get_group_info(group_id=group_id)
        group_name = group_info["group_name"]
        group_name_dict[group_id] = group_name
        with open("./group.json", "w", encoding="utf-8") as f:
            json.dump(group_name_dict, f)
        return group_name


@mc.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    group_name = await get_group_name(bot, event.group_id)
    if "MC" in group_name or "我的世界" in group_name:
        if event.is_tome():
            await mc.finish(MessageSegment.at(event.user_id) + choice(tome_word))
        ra = randint(1, 100)
        if ra <= 2:
            await mc.finish(MessageSegment.at(event.user_id) + choice(at_word))
        elif ra <= 5:
            await mc.finish(choice(word))
