from nonebot import on_message, on_command
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent
)
from utils.utils import DailyCountLimiter, ConfigReader

from .data_source import get_love

config = ConfigReader("JiaoYuan")
hello = DailyCountLimiter(1)

answer = {
    "学校地址": "湖南省长沙市长沙县黄兴镇 湖南交通职业技术学院(校内)",
    "军训": "军训半个月,期间不能染发,男生一律寸头,穿黑袜子,不要顶撞教官,一人生病全连吃药,身上有伤提供证明可以去伤病连",
    "晚自习": "整个大一都要上晚自习,周五周六不上,晚自习时间:19:15 - 20:50,晚自习有学生会检查,上交手机并清点数量,不能带耳机听歌,不能聊天,建议买两本小说看",
    "空调": "所有寝室都有空调,空调的费用会算在住宿费里,空调要出电费(电费0.6元/度),教室也有空调!",
    "洗衣机": "宿舍楼每层都有洗衣机,洗衣费用3-6元",
    "公交": "学校有一路公交车X112,整点去一般都有车,30分钟到杜家坪地铁站",
    "地铁": "最近的地铁站是杜家坪地铁站,建议使用湘行一卡通或长沙地铁",
    "黑车": "黑车一般往返光达地铁站和交院,黑车价格15以下就能走,多一块钱都是坑,态度硬点讲价能讲到10",
    "上课": "一天四大节课,一小节课45分钟\n上午08:30-12:10\n下午13:30-17:00\n晚自习19:15-20:50\n周二下午一般没课",
    "示范寝": "整个大一都要搞示范寝,入学会交代示范寝标准,示范寝前两个月很严,越后面越敷衍",
    "查寝": "早上阿姨检查寝室内务,晚上督导部检查人数",
    "交院全景": "链接http://720yun.com/t/07525mz8cev?pano_id=398535",
    "开学日期": "9月2日(星期六),老生报道\n9月2日(星期六)-3日(星期日),老生补考\n9月4日(星期一),老生开课\n9月6日(星期三)-7日(星期四),新生报道",
    "寝室": "交院大部分寝室都是5人寝,最多6人一寝,寝室按报道的顺序分配,床位先到先得,有一个上床下桌,同班同寝(有极少的混寝)",
    "校园网": "校园网240一张卡,不充话费能用一学期,送一学期校园网,能连校园WIFI和寝室宽带,需要花钱买双绞线",
    "驾校": "别报国大,垃圾驾校"
}

regular_answer = {
    ""
}

chat = on_message(priority=10)


@chat.handle()
async def chat_handle(event: GroupMessageEvent):
    if event.group_id in config["jiao_groups"]:
        say = event.message.extract_plain_text()
        if say == "交院帮助":
            await chat.finish("交院帮助列表:\n" + " ; ".join(answer))
        elif say in answer.keys():
            msg = answer[say]
            await chat.finish(msg)


luck = on_command("今日桃花", priority=6, block=True)


@luck.handle()
async def luck_handle(bot: Bot, event: GroupMessageEvent):
    if event.group_id not in config["jiao_groups"]:
        return

    msg = get_love(event.user_id, event.sender.sex)
    await bot.send(
        at_sender=True,
        event=event,
        message=msg,
    )


aunt = on_message(priority=10)


@aunt.handle()
async def aunt_handle(bot: Bot, event: GroupMessageEvent):
    if event.group_id in config["jiao_groups"] and event.user_id == 2158755390 and hello.check(2158755390):
        hello.increase(2158755390)
        await aunt.finish("阿姨好")

    if event.group_id in config["jiao_groups"] and event.user_id == 294608708 and hello.check(294608708):
        hello.increase(294608708)
        await aunt.finish("吊毛来了")

    if event.group_id in config["jiao_groups"] and event.user_id == 484650164 and hello.check(484650164):
        hello.increase(484650164)
        await aunt.finish("富婆好")
