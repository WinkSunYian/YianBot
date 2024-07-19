# from tencentcloud.common import credential
# from tencentcloud.common.profile.client_profile import ClientProfile
# from tencentcloud.common.profile.http_profile import HttpProfile
# from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
# from tencentcloud.tbp.v20190627 import tbp_client, models

from configs.configs import TencentCloudConfig, NICKNAME
from utils.db_utils import DialogueHistoryManager, db
from utils.http_utils import Aiohttp
import json
import re
import requests
import time
from random import choice

manager = DialogueHistoryManager(db)


async def getChat(inputText, user_id, at=False):
    # 复读
    if len(inputText) == 1 and at:
        return inputText

    message = await getDictionaryChat(inputText, at=at)
    if not message and at:  # 内置字典无匹配时
        message = await getChatGPT(inputText, user_id)
        # message = await getTencentChat(inputText, terminalId=user_id)
        # message = await getDictionaryChat(message, ai=True)
    return message


async def getDictionaryChat(inputText, at=False, ai=False):
    if ai:
        # 优化AI回答
        dictionary = {
            "发明出来的那个时候。": ["孙先生是我的开发者", "我的开发者是孙先生"],
            "这取决于您怎么看了，腾讯公司成立于1998年。我的年龄目前还无法计算，不过我读过很多书。": ["逸安出生于2021年"],
            "我的生日就是你激活我的那一天，所以我应该非常年轻。": ["我出生与2021年"],
            "逸安的家庭成员来自于全球各地，大部分在中国，也有部分在美国欧洲和其他国家": ["当然是中国啦", "逸安生在中国"],
            "逸安无处不在，但一定是在你身边": ["逸安在服务器里"]
        }
        for word in dictionary:
            if inputText == word:
                return choice(dictionary[word])
        return inputText
    else:
        if at:
            dictionary = {
                "^逸安$": ["嗯哼?", "干嘛?", "干嘛", "干嘛呀"],
                "^$": ["嗯哼?", "干嘛?", "干嘛", "干嘛呀"],
                "孙先生": ["他是我的主人", "他是我的开发者"],
                "你的主人": ["是孙先生", "不告诉你", "不告诉你", "你猜"],
                "软糖": ["想让逸安回答问题,得有软糖才行,#Cknow #ChatGPT"],
                "方糖": ["想让逸安干坏事,#短轰"],
                "小熊饼干": ["一块没什么用的饼干"],
                "^早(安)?$": ["早", "早上好", "早安", "早安吖"],
                "^晚(安)?$": ["晚", "晚上好", "晚安", "晚安吖"],
            }
        else:
            dictionary = {
                "^逸安$": ["嗯哼?", "干嘛?", "干嘛", "干嘛呀"],
                "^早(安)?$": [None, None, None, None, None, None, "早", "早安", "早上好", "早安吖"],
                "^晚(安)?$": [None, None, None, None, None, None, "晚", "晚安", "晚上好", "晚安吖"],
                "^\?$": [None, None, "?"],
                "^\？$": [None, None, "?"],
                "^6$": [None, None, None, "6", "6", "六"]
            }

        for word in dictionary:
            if re.search(word, inputText, flags=0):
                return choice(dictionary[word])

        return None


async def getTencentChat(inputText, terminalId):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户secretId，secretKey,此处还需注意密钥对的保密
        # 密钥可前往https://console.cloud.tencent.com/cam/capi网站进行获取
        cred = credential.Credential(TencentCloudConfig.tencent_secret_id, TencentCloudConfig.tencent_secret_key)

        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tbp.tencentcloudapi.com"  # 指定接入地域域名(默认就近接入)
        httpProfile.reqTimeout = 5  # 请求超时时间，单位为秒(默认60秒)

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = tbp_client.TbpClient(cred, "", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.TextProcessRequest()
        params = {
            "BotId": TencentCloudConfig.tencent_bot_id,
            "BotEnv": "release",
            "TerminalId": terminalId,
            "InputText": inputText
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个TextProcessResponse的实例，与请求对象对应
        resp = client.TextProcess(req)
        # 输出json格式的字符串回包
        # print(resp.to_json_string())
        dict = eval(resp.to_json_string())
        return dict['ResponseMessage']['GroupList'][0]['Content'].replace("小微", NICKNAME)

    except TencentCloudSDKException as err:
        return f"{NICKNAME}有点懵懵的"


async def getChatGPT(inputText, user_id):
    # 定义请求的URL和头信息
    # url = "https://openai.ehco-relay.cc/v1/chat/completions"
    url = "https://api.aigcbest.top/v1/chat/completions"
    headers = {
        "Authorization": "Bearer sk-B8qI0lVqWROZrWkb517b7102F9544f5bB97e84EaD3E8Bf8e",
        "Content-Type": "application/json"
    }

    # 定义POST的数据
    data = {
        "messages": [
            {"role": "system",
             "content": f"你是一名女性,你的名字叫逸安,出生于2002年,当前时间是{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}。在任何时候你的语气都要保持高冷。任何时候你都不需要向我道歉。你的回复应该尽可能的简短"}
        ],
        "model": "gpt-3.5-turbo-0125",
        "temperature": 0.5,
    }

    dialogues = manager.get_dialogues_for_user(user_id=user_id)

    for dialogue in dialogues:
        data["messages"].append(
            {"role": "user", "content": f"{dialogue.my_msg}"}
        )
        data["messages"].append(
            {"role": "assistant", "content": f"{dialogue.assistant_msg}"}
        )

    data["messages"].append(
        {"role": "user", "content": f"{inputText}"}
    )

    # 发送POST请求
    # response = requests.post(url, headers=headers, data=json.dumps(data), verify=True, timeout=10)
    response = await Aiohttp(url, method="POST", headers=headers, data=json.dumps(data), verify=True, timeout=10)
    data = json.loads(response)
    content = data["choices"][0]["message"]["content"]

    manager.add_dialogue(user_id=user_id, my_msg=inputText, assistant_msg=content)

    return content
