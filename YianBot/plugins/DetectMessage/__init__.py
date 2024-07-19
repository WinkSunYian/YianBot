from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.message import event_preprocessor
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    PrivateMessageEvent,
    Message
)
from .data_source import text_review
from utils.utils import args_split, get_message_text
from configs.configs import MASTER
import json

__plugis__enable__group1__ = [
    # 交院
    868418917,
    162379991,
    879123689,
    737989924,
    460282432,
    703841240,
    463213155,
    # 水利水电
    114563902,
    # 林科大
    770143004,
    # 中医药
    708316791,
    # 环境保护
    872175975,
    # 长沙理工
    741013409

]

__plugis__enable__group2__ = [
    # 湖南都市职业学院
    603275358,
    # 湖南艺术职业学院
    705459638
]

__plugin__name__ = "DetectMessage"


def read_config():
    with open(f"plugins\\{__plugin__name__}\\config.json", encoding='utf-8-sig') as fp:
        return json.load(fp)


def write_config(data):
    with open(f"plugins\\{__plugin__name__}\\config.json", "w", encoding='utf-8-sig') as fp:
        json.dump(data, fp)


@event_preprocessor
async def event_preprocessor_handle(bot: Bot, event: GroupMessageEvent):
    if event.group_id in __plugis__enable__group1__:  # 群是否启用插件
        self_role = (await bot.get_group_member_info(
            group_id=event.group_id,
            user_id=event.self_id
        ))['role']
        if len(str(event.message)) >= 15:  # 不审核10字以下的内容
            if self_role in ['admin', 'owner']:  # Bot在群内是否为管理员
                if event.sender.role not in ['admin', 'owner']:  # 检查消息发送者是否为管理员
                    audit_results = await text_review(event.message.extract_plain_text())
                    if "conclusion" in audit_results.keys():
                        if audit_results["conclusion"] == "不合规":  # 检测消息是否违规
                            config = read_config()
                            if str(event.user_id) not in config:
                                config[str(event.user_id)] = 60
                            else:
                                config[str(event.user_id)] *= 6
                            write_config(config)

                            await bot.delete_msg(message_id=event.message_id)  # 撤回消息

                            if config[str(event.user_id)] >= 2592000:  # 如果时长大于30天
                                await bot.send(
                                    event=event,
                                    message=f"已将{event.user_id}踢出群聊"
                                )
                                await bot.set_group_kick(  # 移除群聊
                                    group_id=event.group_id,
                                    user_id=event.user_id,
                                    reject_add_request=True  # 是否拉黑
                                )
                            else:
                                await bot.send(
                                    event=event,
                                    message=f"{event.user_id}发广告被我逮住了,禁言{config[str(event.user_id)]}秒"
                                )
                                await bot.set_group_ban(
                                    group_id=event.group_id,
                                    user_id=event.user_id,
                                    duration=config[str(event.user_id)]
                                )
    elif event.group_id in __plugis__enable__group2__:
        self_role = (await bot.get_group_member_info(
            group_id=event.group_id,
            user_id=event.self_id
        ))['role']
        thesaurus = [
            "加QQ",
            "扩列",
            "全体成员",
            "重要通知",
            "进QQ群",
            "代刷",
            "刷课",
            "校园通知",
            "资料",
            "勤工俭学",
            "兼职",
            "暑假工",
            "代写",
            "菜鸟驿站"
        ]
        if len(str(event.message)) >= 10:  # 不审核10字以下的内容
            if self_role in ['admin', 'owner']:  # Bot在群内是否为管理员
                if event.sender.role not in ['admin', 'owner']:  # 检查消息发送者是否为管理员
                    if "加下我" in event.message.extract_plain_text():
                        await bot.delete_msg(message_id=event.message_id)  # 撤回消息
                    else:
                        for i in thesaurus:
                            if i in event.message.extract_plain_text():
                                await bot.delete_msg(message_id=event.message_id)  # 撤回消息
                                break


test = on_command("#test", priority=5, block=True)


@test.handle()
async def test_handle(bot: Bot, event: PrivateMessageEvent, args: Message = CommandArg()):
    code = await text_review(event.message.extract_plain_text())
    await test.finish(f"{event.message.extract_plain_text()}\n\n{code}")
