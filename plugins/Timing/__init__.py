from nonebot import (
    require,
    get_bots
)
import asyncio
from random import randint

__plugin_name__ = 'Timing'
__plugin_usage__ = '用法：在规定时间触发发送的信息。'

"""
# 设置一个定时器
timing = require("nonebot_plugin_apscheduler").scheduler



# 设置在15:00发送信息
@timing.scheduled_job("cron", hour='19', minute='28', id="time")
async def time():
    bot, = get_bots().values()
    # 发送一条群聊信息
    await bot.send_msg(
        message_type="group",
        # 群号
        group_id=162379991,
        message='22.01'
    )

    # 随机休眠2-5秒
    await asyncio.sleep(randint(2, 5))

    # 发送一条私聊信息
    await bot.send_msg(
        message_type="private",
        # 私聊用户QQ号
        user_id=858386910,
        message='傻逼'
    )


# 设置在08:30发送信息
moring = require("nonebot_plugin_apscheduler").scheduler


@moring.scheduled_job("cron", hour='8', minute='30', id="moring_scheduled_job")
async def moring_scheduled_job():
    # 发送一条私聊信息
    bot, = get_bots().values()
    await bot.send_msg(
        message_type="private",
        # 私聊用户QQ号
        user_id=2074731829,
        message='早安'
    )

# 设置在22:00发送信息
night = require("nonebot_plugin_apscheduler").scheduler


@night.scheduled_job("cron", hour='22', minute='00', id="night_scheduled_job")
async def night_scheduled_job():
    # 发送一条信息
    bot, = get_bots().values()
    await bot.send_msg(
        message_type="private",
        # 私聊用户QQ号
        user_id=2074731829,
        message='晚安'
    )


flatterer = require("nonebot_plugin_apscheduler").scheduler


# 设置在21:40发送消息
@flatterer.scheduled_job("cron", hour='21', minute='40', id="fla")
async def fla():
    data = datetime.now()
    print(os.getcwd())
    file = open(r"D:\SunYiAn\StorageBox\Python\YianBot\YianBot\yianbot\res\flatterer.txt", 'r', encoding="utf-8")
    content = file.read()
    list = content.split("\n")
    rand = randint(0, len(list) - 1)
    msg = "舔狗日记 {}月{}日 {}".format(data.month, data.day, weather("长沙")["wea"]) + "\n" + list[rand]
    file.close()

    bot, = get_bots().values()
    # 发送一条群聊信息
    print(msg)
    await bot.send_msg(
        message_type="group",
        # 群号
        group_id=162379991,
        message=msg
    )
    await bot.send_msg(
        message_type="group",
        # 群号
        group_id=157579630,
        message=msg
    )


def weather(city):
    url = "https://api.iyk0.com/tq/?city={}".format(city)
    dict = eval(get(url).text)
    return dict

"""
