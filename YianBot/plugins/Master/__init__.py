from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    Message,
    MessageSegment,
    GroupMessageEvent,
)
from nonebot.params import CommandArg
import time
import os
from utils.utils import args_split, ConfigReader
from YianBot.configs.Config import MASTER
from utils.http_utils import Aiohttp
import json

__plugin_name__ = "Master"
__plugin_usage__ = "主人功能"


user_tags = on_command("#用户标签", priority=5, block=True)


@user_tags.handle()
async def tags_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    if event.user_id == MASTER:
        args_list = args_split(args)
        if args_list[0] == "添加":
            if len(args_list) < 3:
                await user_tags.finish("缺少参数")
            if len(args_list) < 4:
                args_list.append("{}")
            url = "http://api.sunyian.cloud/add-user-tag/"
            headers = {"API-Key": "jix8ZqQlAle43JyjDqgpllmO7LOvwzEz"}
            data = {
                "qq_id": args_list[1],
                "tag_name": args_list[2],
                "extra_data": json.loads(args_list[3]),
            }
            response = await Aiohttp(
                url,
                method="POST",
                headers=headers,
                json=data,
                verify=True,
                timeout=10,
            )
            await user_tags.finish(response["message"])
        elif args_list[0] == "删除":
            url = "http://api.sunyian.cloud/remove-user-tag/"
            headers = {"API-Key": "jix8ZqQlAle43JyjDqgpllmO7LOvwzEz"}
            data = {"qq_id": args_list[1], "tag_name": args_list[2]}
            response = await Aiohttp(
                url,
                method="POST",
                headers=headers,
                json=data,
                verify=True,
                timeout=10,
            )
            await user_tags.finish(response["message"])
        elif args_list[0] == "查询":
            url = "http://api.sunyian.cloud/list-user-tag/"
            headers = {"API-Key": "jix8ZqQlAle43JyjDqgpllmO7LOvwzEz"}
            data = {"qq_id": args_list[1]}
            response = await Aiohttp(
                url,
                method="POST",
                headers=headers,
                json=data,
                verify=True,
                timeout=10,
            )
            if response["code"] == 0:
                await user_tags.finish(response["message"])
            tag_list = response["tag_list"]
            if len(tag_list) == 0:
                await user_tags.finish("该用户没有标签")
            s = f"{args_list[1]}的标签："
            for i in tag_list:
                s += "\n"
                s += i["tag_name"]
                for j in i["extra_data"]:
                    s += f"\n    {j}:{i['extra_data'][j]}"
            await user_tags.finish(s)
        elif args_list[0] == "修改":
            url = "http://api.sunyian.cloud/update-user-tag/"
            headers = {"API-Key": "jix8ZqQlAle43JyjDqgpllmO7LOvwzEz"}
            data = {
                "qq_id": args_list[1],
                "tag_name": args_list[2],
                "extra_data": json.loads(args_list[3]),
            }
            response = await Aiohttp(
                url,
                method="POST",
                headers=headers,
                json=data,
                verify=True,
                timeout=10,
            )
            if response["code"] == 0:
                await user_tags.finish(response["message"])
            await user_tags.finish(response["message"])


group_list = on_command("#群列表", priority=5, block=True)


@group_list.handle()
async def group_list_handle(bot: Bot, event: MessageEvent):
    if event.user_id == MASTER:
        for group in await bot.get_group_list():
            msg = "{}\n{}".format(group["group_name"], group["group_id"])
            await bot.send(event=event, message=msg)


message_send = on_command("#发群消息", priority=5, block=True)


@message_send.handle()
async def message_send_handle(
    bot: Bot, event: MessageEvent, args: Message = CommandArg()
):
    if event.user_id == MASTER:
        text = args[0].data["text"]
        group = int(text.split(" ")[0])
        msg = text.split(" ")[1]
        await bot.send_msg(message_type="group", group_id=group, message=msg)


info = on_command("#info")


@info.handle()
async def info_handle(bot: Bot, event: GroupMessageEvent, args: Message = CommandArg()):
    if event.user_id == MASTER:
        args_list = args_split(args, 1)
        data = await bot.get_group_member_info(
            group_id=event.group_id, user_id=args_list[0]
        )
        msg = f"nickname:{data['nickname']}\nuser_id{data['user_id']}\nrole:{data['role']}\nlever:{data['level']}\njoin_time:{time.strftime('%Y-%m-%d %H:%M.%S', time.localtime(data['join_time']))}"
        await info.finish(MessageSegment.reply(event.user_id) + msg)


plugin_list = on_command("#插件", aliases={"/插件"}, block=True)


@plugin_list.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    if event.user_id == MASTER:
        args_list = args_split(args)
        if len(args_list) == 0:
            msg = """
            状态
            配置 查看 [插件名]
            配置 修改 [插件名] [项] [值]
            """
            await plugin_list.finish(msg)
        elif args_list[0] == "状态":
            msg_list = []
            for plugin in os.listdir("plugins/"):
                if "_" in plugin:
                    continue
                config = ConfigReader(plugin)
                msg_list.append(
                    "%s\t\t%s"
                    % (plugin, "启用" if config["plugin"] == "enable" else "停用")
                )
            await plugin_list.finish("\n".join(msg_list))
        elif args_list[0] == "配置":
            if args_list[1] == "查看":
                config = ConfigReader(args_list[2])
                await plugin_list.finish(str(config))
            elif args_list[1] == "修改":
                config = ConfigReader(args_list[2])

                if args_list[3] == "plugin":
                    args_list[4] = "enable" if args_list[4] == "enable" else "disable"

                if args_list[3] in config:
                    config[args_list[3]] = args_list[4]
                    await plugin_list.finish(str(config))
                else:
                    await plugin_list.finish("不存在的项")
            elif args_list[1] == "增加":
                config = ConfigReader(args_list[2])
                config[args_list[3]] = args_list[4]
                await plugin_list.finish(str(config))
            elif args_list[1] == "删除":
                config = ConfigReader(args_list[2])
                del config[args_list[3]]
                await plugin_list.finish(str(config))
