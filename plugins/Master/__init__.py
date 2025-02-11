from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    Message,
    MessageSegment,
    GroupMessageEvent,
)
from nonebot.params import CommandArg, Depends
import time
import os
from utils.utils import args_split, ConfigReader
from utils.http_utils import http_client
from dependencies import get_args_list
from configs.Config import MASTER

__plugin_name__ = "Master"
__plugin_usage__ = "主人功能"


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


tag = on_command("#tag", block=True)


@tag.handle()
async def _(bot: Bot, event: GroupMessageEvent, args_list=Depends(get_args_list)):
    if event.user_id == MASTER:
        
        status, response = await http_client.post(
            f"/users/{args_list[0]}/tags",
            json={"name": args_list[1], "expiry_date": args_list[2]},
        )
        if status == 201:
            await tag.finish(f"添加标签成功")
        else:
            await tag.finish(f"添加标签失败，{response}")


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
