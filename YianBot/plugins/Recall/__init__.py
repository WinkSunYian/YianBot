from nonebot.adapters.onebot.v11 import (
    Bot,
    Event,
    GroupRecallNoticeEvent,
    Message
)
from nonebot.plugin import on_notice
from nonebot.rule import Rule
from nonebot.typing import T_State
import os

__plugin_name__ = 'Recall'
__plugin_usage__ = '防撤回'

SELFPATH = os.getcwd() + "\\yianbot\\plugins\\Bombardment\\"


async def _checker(bot: Bot, event: Event, state: T_State) -> bool:
    return isinstance(event, GroupRecallNoticeEvent)


def to_cq(list):
    CQ = "撤回了消息但被我发现了\n——————————————\n"
    for data in list:
        print(data)
        if data['type'] == "text":
            CQ = CQ + data['data']['text']
        if data['type'] == "face":
            CQ = CQ + "[CQ:face,id={}]".format(data['data']['id'])
        if data['type'] == "image":
            CQ = CQ + "[CQ:image,file={}]".format(data['data']['url'])

    return CQ


recall = on_notice(priority=5, rule=Rule(_checker))


@recall.handle()
async def recall_handle(bot: Bot, event: GroupRecallNoticeEvent, state: T_State):
    user_id = event.user_id
    operator_id = event.operator_id #操作员ID
    group_id = event.group_id
    if user_id != operator_id:
        return

    if user_id in [7345222]:
        return

    if group_id in [868418917] or True:
        return

    die_mess = await bot.call_api('get_msg', **{
        'message_id': event.message_id
    })

    msg = to_cq(die_mess['message'])
    await recall.send(
        at_sender=True,
        message=Message(msg)
    )
