from nonebot import on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    MessageSegment,
    Message
)
from nonebot.params import (
    CommandArg
)
from utils.utils import (
    args_split
)
from utils.db_utils import UserBackpackManager
from utils.utils import FreqLimiter
from .data_source import get_card, concatenate_images, get_random_filenames, calculate_bull_for_two_groups

__plugin_name__ = 'Bullfighting'
__plugin_usage__ = '斗牛'

play = FreqLimiter(5)

cattle_list = ["马", "丁", "二", "三", "四", "五", "六", "七", "八", "九", "牛"]

_ = on_command("#斗牛", priority=5, block=True)


@_.handle()
async def __(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    args_list = args_split(args, 1)
    """
    args_list[0] : 金额
    """
    if args_list[0] in ["梭哈", "all", "allin"]:
        backpack = UserBackpackManager(event.user_id)
        args_list[0] = int(backpack["软妹币"] / 3)

    if len(args_list) == 0:
        await _.finish("不压钱?")
    elif not isinstance(args_list[0], int):
        await _.finish("只能压整数,啥卵")
    elif args_list[0] < 10:
        await _.finish("压这点,谁跟你玩?最少压10")
    else:
        if play.check(event.user_id):
            play.start_cd(event.user_id)
            backpack = UserBackpackManager(event.user_id)

            if args_list[0] * 3 > backpack["软妹币"]:
                await _.finish("穷狗,你钱不够")

            cards = get_random_filenames()
            result = calculate_bull_for_two_groups(cards)
            money = args_list[0]
            if result[0] >= result[1]:
                money *= -1
                if result[0] == 8 or result[0] == 9:
                    money *= 2
                elif result[0] == 10:
                    money *= 3
                else:
                    money *= 1
            else:
                if result[1] == 8 or result[1] == 9:
                    money *= 2
                elif result[1] == 10:
                    money *= 3
                else:
                    money *= 1
            try:
                img = "file:///" + concatenate_images(cards)
                backpack["软妹币"] += money
            except:
                await _.finish("你遇到了一个bug\nps:这个bug极其诡异,我根本不知道怎么修复这个bug")
            await _.finish(
                MessageSegment.image(
                    img) + f"牛{cattle_list[result[0]]}     牛{cattle_list[result[1]]}\n本次收益：{money}")
        else:
            await _.finish(MessageSegment.reply(event.message_id) + "赌这么快,准备去天台吗?")
