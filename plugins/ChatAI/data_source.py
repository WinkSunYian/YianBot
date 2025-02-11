from configs.Config import NICKNAME
from utils.http_utils import http_client
import re
from random import choice


def to_messages(data: dict):
    messages = []
    for message in data["messages"]:
        raw_message = (
            message["raw_message"].replace("[CQ:at,qq=1012896426]", "@逸安").strip()
        )
        if message["user_id"] == message["self_id"]:
            messages.append({"role": "assistant", "content": raw_message})
        else:
            messages.append({"role": "user", "content": raw_message})
    return messages


async def getChat(inputText, user_id, at=False):
    # 复读
    if len(inputText) == 1 and at:
        return inputText

    message = await getDictionaryChat(inputText, at=at)
    if not message and at:  # 内置字典无匹配时
        message = await getChatGPT(inputText, user_id)
    return message


async def getDictionaryChat(inputText, at=False):
    if at:
        dictionary = {
            "^逸安$": ["说", "何事", "干嘛", "怎?"],
            "^$": ["说", "何事", "干嘛", "怎?"],
            "孙先生": ["他是我的主人", "他是我的开发者"],
            "你的主人": ["是孙先生", "不告诉你", "不告诉你", "你猜"],
        }
    else:
        dictionary = {
            "^逸安$": ["说", "何事", "干嘛", "怎?"],
            "^\?$": [None, None, "?"],
            "^\？$": [None, None, "?"],
            "^6$": [None, None, None, "6", "6", "六"],
        }

    for word in dictionary:
        if re.search(word, inputText, flags=0):
            return choice(dictionary[word])

    return None


async def getChatAIresponse(result, user_id):
    data = to_messages(result)
    status, response = await http_client.post(
        f"/users/{user_id}/chat-ai", json={"messages": data}
    )
    response = response["data"]["response"]
    return response
