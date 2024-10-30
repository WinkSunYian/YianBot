from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment, Message
from nonebot.params import CommandArg
from utils.utils import args_split
from utils.utils import FreqLimiter
from YianBot.configs.Config import MASTER

__plugin_name__ = "ItemRank"
__plugin_usage__ = "道具排行"

cd = FreqLimiter(300)

_ = on_command("#排行", priority=5, block=True)


@_.handle()
async def __(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    pass
    # if cd.check(event.user_id):
    #     cd.start_cd(event.user_id)
    #     with db_session:
    #         top_items = select(i for i in Item if i.backpack.user.user != MASTER).order_by(desc(Item.quantity)).limit(
    #             9)
    #         rank_text = "软妹币排行\n"
    #         for i, item in enumerate(top_items, start=1):
    #             us = await bot.get_stranger_info(user_id=item.backpack.user.user)
    #             rank_text += f"Top{i}: {us['nickname']:6.5}{item.backpack.user.user:10} -: {item.quantity}枚\n"
    #         await _.finish(rank_text)
    # else:
    #     await _.finish(MessageSegment.reply(event.message_id) + f"命令冷却中,剩余{cd.left_time(event.user_id):.0f}秒")
