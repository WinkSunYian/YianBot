from requests import get
import json
from YianBot.configs.Config import NICKNAME

config = {
    "lanlanhz": {
        "key": "6da0187a04cf63dde1c7a90652f267b0",
        "url": "http://lanlanhz.mf0a.cn/api/index/submit?key={key}&phone={phone}&time={time}",
        "max": 10
    },
    # 小南瓜3540689144
    "yhbox": {
        "key": "ad72ca9c2387c31f030fa59aa72ddeb7",
        "url": "http://sms.yhbox.site/api/submit/{key}/{phone}/{time}",
        "max": 30
    },
    # 2490791950短信轰炸lxsms.top
    "lxsms": {
        "key": "78f58185b72cb7c70b04c81c45960395",
        "url": "http://lxsms.top/api/index/submit?key={key}&phone={phone}&time={time}",
        "max": 30
    },
    "qivi": {
        "key": "328842a50e1dfbf5b14954e11982f931",
        "url": "http://121.62.19.29:12222/api/index/submit?key={key}&phone={phone}&time={time}",
        "max": 9999
    }
}


async def submitBombingRequest(phone, time):
    # noinspection PyBroadException
    try:
        url = config["qivi"]["url"].format(key=config["qivi"]["key"], phone=phone,
                                           time=time)
        html = get(url, timeout=5).text
        data = json.loads(html)
        if data['msg'].find("成功") != -1:
            code = -1
            msg = f"{NICKNAME}成功向{phone}派遣了轰炸机,轰炸时间{time}分钟\n消耗了方糖 * {time}"
        elif data['msg'].find("续费") != -1:
            code = -1
            msg = "短轰服务器维护中"
        elif data['msg'].find("重复"):
            code = -1
            msg = "他的轰炸还没结束呢"
        else:
            code = -1
            msg = "无法连接至服务器"
        return code, msg
    except:
        return -1, "轰炸指挥部没有接电话呢,过会再来打给他吧"
