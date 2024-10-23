from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    Message,
    MessageSegment
)
from nonebot.params import (
    CommandArg
)
from utils.utils import get_message_at
from YianBot.configs.Config import MASTER
from random import choice

__plugin_name__ = 'EvaluateIt'
__plugin_usage__ = '骂人'

scold_thesaurus = [
    "你妈biu",
    "大傻呗",
    "傻呗",
    "敲你吗!敲你吗!",
    "你这个丑陋的土拨鼠",
    "大傻呗 我tui~",
    "你长得像我邻居家种的马铃薯",
    "你个大制杖",
    "你个番薯",
    "你个大制杖"
]

praise_thesaurus = [
    "你她娘的还真是个天才"
]

scold = on_command("骂", aliases={'骂他', '骂她', '骂它'}, priority=6, block=True)


@scold.handle()
async def scold_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    qq_list = get_message_at(args)
    if MASTER in qq_list:
        msg = MessageSegment.at(event.user_id) + MessageSegment.text("哼~ 我怎么可能会骂我的主人呢")
        await scold.finish(msg)
    elif event.is_tome():
        msg = MessageSegment.at(event.user_id) + MessageSegment.text("???骂我干嘛")
        await scold.finish(msg)
    else:
        for qq in qq_list:
            text = choice(scold_thesaurus)
            msg = MessageSegment.at(qq) + MessageSegment.text(text)
            await scold.finish(msg)


praise = on_command("夸", aliases={'夸他', '夸她', '夸它'}, priority=6, block=True)


@praise.handle()
async def scold_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    qq_list = get_message_at(args)
    if MASTER in qq_list:
        msg = MessageSegment.at(event.user_id) + MessageSegment.text("主人最聪明啦")
        await praise.finish(msg)
    elif event.is_tome():
        msg = MessageSegment.at(event.user_id) + MessageSegment.text("谢谢啦")
        await praise.finish(msg)
    else:
        for qq in qq_list:
            text = choice(praise_thesaurus)
            msg = MessageSegment.at(qq) + MessageSegment.text(text)
            await praise.finish(msg)
