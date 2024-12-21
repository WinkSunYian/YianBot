from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment
from nonebot.matcher import matchers, Matcher
from nonebot.exception import IgnoredException
from datetime import datetime
from collections import defaultdict
from nonebot import require
from typing import List, Union, Optional, Type, Any
import httpx
import nonebot
import pytz
import time
import json
import os
import re

# scheduler = require("nonebot_plugin_apscheduler").scheduler


class CountLimiter:
    """
    次数检测工具，检测调用次数是否超过设定值
    """

    def __init__(self, max_count: int):
        self.count = defaultdict(int)
        self.max_count = max_count

    def add(self, key: Any):
        self.count[key] += 1

    def check(self, key: Any) -> bool:
        if self.count[key] >= self.max_count:
            self.count[key] = 0
            return True
        return False


class UserBlockLimiter:
    """
    检测用户是否正在调用命令
    """

    def __init__(self):
        self.flag_data = defaultdict(bool)
        self.time = time.time()

    def set_true(self, key: Any):
        self.time = time.time()
        self.flag_data[key] = True

    def set_false(self, key: Any):
        self.flag_data[key] = False

    def check(self, key: Any) -> bool:
        if time.time() - self.time > 30:
            self.set_false(key)
            return False
        return self.flag_data[key]


class FreqLimiter:
    """
    命令冷却，检测用户是否处于冷却状态
    """

    def __init__(self, default_cd_seconds: int):
        self.next_time = defaultdict(float)
        self.default_cd = default_cd_seconds

    def check(self, key: Any) -> bool:
        return time.time() >= self.next_time[key]

    def start_cd(self, key: Any, cd_time: int = 0):
        self.next_time[key] = time.time() + (
            cd_time if cd_time > 0 else self.default_cd
        )

    def left_time(self, key: Any) -> float:
        return self.next_time[key] - time.time()


class BanCheckLimiter:
    """
    恶意命令触发检测
    """

    def __init__(self, default_check_time: float = 5, default_count: int = 4):
        self.mint = defaultdict(int)
        self.mtime = defaultdict(float)
        self.default_check_time = default_check_time
        self.default_count = default_count

    def add(self, key: Union[str, int, float]):
        if self.mint[key] == 1:
            self.mtime[key] = time.time()
        self.mint[key] += 1

    def check(self, key: Union[str, int, float]) -> bool:
        if time.time() - self.mtime[key] > self.default_check_time:
            self.mtime[key] = time.time()
            self.mint[key] = 0
            return False
        if (
            self.mint[key] >= self.default_count
            and time.time() - self.mtime[key] < self.default_check_time
        ):
            self.mtime[key] = time.time()
            self.mint[key] = 0
            return True
        return False


class DailyCountLimiter:
    """
    每日调用次数限制
    """

    tz = pytz.timezone("Asia/Shanghai")

    def __init__(self, max_count):
        self.today = -1
        self.count = defaultdict(int)
        self.max_count = max_count

    def check(self, key) -> bool:
        day = datetime.now(self.tz).day
        if day != self.today:
            self.today = day
            self.count.clear()
        return bool(self.count[key] < self.max_count)

    def get_num(self, key):
        return self.count[key]

    def increase(self, key, count=1):
        self.count[key] += count

    def decrease(self, key, count=1):
        self.count[key] -= count

    def reset(self, key):
        self.count[key] = 0


class DailyBalanceLimiter:
    """
    每日余额限制
    """

    tz = pytz.timezone("Asia/Shanghai")

    def __init__(self, max_balance):
        self.today = -1
        self.balance = defaultdict(lambda: max_balance)

    def check(self, key, number) -> bool:
        day = datetime.now(self.tz).day
        if day != self.today:
            self.today = day
            self.balance.clear()
        return bool((self.balance[key] - number) >= 0)

    def spend(self, key, number):
        self.balance[key] -= number

    def earn(self, key, number):
        self.balance[key] += number

    def get_num(self, key):
        self.check(key, 0)
        return self.balance[key]


class DialogueControl:
    """
    对话记录工具
    """

    dialogue_path = "data\\dialogue\\{}.json"

    data: list = []

    def __init__(self, user_id):
        self.user_dialogue = self.dialogue_path.format(user_id)
        if not os.path.exists(self.user_dialogue):
            with open(self.user_dialogue, "w", encoding="utf-8-sig") as fp:
                json.dump([], fp)
        self.read_dialogue()

        # 记录用户最后一次使用类的时间
        self.last_used_time = time.time()

    def add(self, user, assistant):
        self.check_last_used_time()  # 检查最后使用时间并清空对话记录

        self.data.append({"role": "user", "content": user})
        self.data.append({"role": "assistant", "content": assistant})
        if len(self.data) / 2 > 5:
            self.data.pop(0)
            self.data.pop(0)

        with open(self.user_dialogue, "w", encoding="utf-8-sig") as fp:
            json.dump(self.data, fp, ensure_ascii=False)

            # 更新用户最后一次使用类的时间
        self.last_used_time = time.time()

    def delete(self):
        with open(self.user_dialogue, "w", encoding="utf-8-sig") as fp:
            fp.write("[]")

    def read_dialogue(self):
        with open(self.user_dialogue, encoding="utf-8-sig") as fp:
            self.data = json.load(fp)

    def check_last_used_time(self):
        # 获取当前时间
        current_time = time.time()

        # 计算时间间隔（单位：秒）
        time_interval = current_time - self.last_used_time

        # 如果时间间隔大于10分钟，则清空对话记录
        if time_interval > 600:
            self.delete()


class ConfigReader:
    """
    配置读取工具
    :param path: 配置地址
    """

    data: json

    def __init__(self, path):
        self.config_path = f"plugins/{path}/config.json"
        self.mtime = 0
        self.read_config()

    def get_mtime(self):
        return os.stat(self.config_path).st_mtime

    def read_config(self):
        if self.mtime != self.get_mtime():
            self.mtime = self.get_mtime()
            with open(self.config_path, encoding="utf-8-sig") as fp:
                self.data = json.load(fp)

    def save_config(self):
        with open(self.config_path, "w", encoding="utf-8-sig") as fp:
            json.dump(self.data, fp, ensure_ascii=False)

    def __getitem__(self, key):
        self.read_config()
        return self.data[key]

    def __setitem__(self, key, value):
        self.read_config()
        self.data[key] = value
        self.save_config()

    def __repr__(self):
        msg_list = []
        for i in self.data:
            msg_list.append(f"{i} : {self.data[i]}")
        return "\n".join(msg_list)

    def __contains__(self, item):
        return item in self.data

    def __delitem__(self, key):
        del self.data[key]


class BackpackControl:
    """
    用户背包工具
    """

    backpack_path = "data\\backpack\\{}.json"

    relational: dict = {}
    data: list = []

    def __init__(self, user_id):
        self.user_backpack = self.backpack_path.format(user_id)
        if not os.path.exists(self.user_backpack):
            with open(self.user_backpack, "w", encoding="utf-8-sig") as fp:
                json.dump([], fp)
        self.read_backpack()
        self.read_relational()

    def save(self):
        with open(self.user_backpack, "w", encoding="utf-8-sig") as fp:
            json.dump(self.data, fp, ensure_ascii=False)

    def read_backpack(self):
        with open(self.user_backpack, encoding="utf-8-sig") as fp:
            self.data = json.load(fp)

    def read_relational(self):
        with open(self.backpack_path.format(0), encoding="utf-8-sig") as fp:
            self.relational = json.load(fp)

    def use_item(self, key: str, number: int) -> int:
        if self[key] >= number > 0:
            self[key] -= number
            return 0
        else:
            return -1

    def get_item(self, key: str, number: int):
        if number > 0:
            self[key] += number
            return 0
        else:
            return -1

    def set_item(self, key: str, number: int):
        self[key] = number

    def query_id(self, key):
        for item in self.relational:
            if key == self.relational[item]:
                return item
        return key

    def query_name(self, key: str) -> str:
        return self.relational[key]

    def __getitem__(self, key):
        key = self.query_id(key)

        for item in self.data:
            if key == item["id"]:
                return item["value"]
        return 0

    def __setitem__(self, key, value):
        key = self.query_id(key)

        for i in range(len(self.data)):
            if key == self.data[i]["id"]:
                if value == 0:
                    del self.data[i]
                else:
                    self.data[i]["value"] = value
                break
        else:
            self.data.append({"id": self.query_id(key), "value": value})
            # 根据ID排序
            self.data = sorted(self.data, key=lambda x: x["id"])
        # 保存背包
        self.save()

    def __repr__(self):
        show = "┏ ━ ━ ━\n"
        if len(self.data) > 0:
            for item in self:
                show += f"┣ {self.query_name(item['id'])} * {item['value']}\n"
        else:
            show += "┣ 空空如也\n"
        show += "┗ ━ ━ ━"
        return show

    def __iter__(self):
        return iter(self.data)


class Checker:
    _instances = {}

    def __new__(cls, plugin_name):
        if plugin_name in cls._instances:
            return cls._instances[plugin_name]
        else:
            instance = super().__new__(cls)
            cls._instances[plugin_name] = instance
            return instance

    _is_init = False

    def __init__(self, plugin_name):
        if not self._is_init:
            self._is_init = True
            self.plugin_name = plugin_name
            self.config = ConfigReader(plugin_name)
            self.public_config = ConfigReader("_PublicConfig")

    def check_config(self):
        if self.config["plugin"] == "enable":
            return True, ""
        else:
            if len(self.config["disableReason"]) > 0:
                return False, self.config["disableReason"]
            else:
                return False, ""

    def check_black(self, user_id) -> bool:
        if user_id in self.public_config["whitelists"]:
            return False
        else:
            return user_id in self.public_config["blacklists"]


async def Checks(matcher: Matcher, event):
    checker = Checker(matcher.plugin_name)
    result = checker.check_config()
    if not result[0]:
        if result[1]:
            await matcher.finish(MessageSegment.reply(event.message_id) + result[1])
        else:
            await matcher.skip()

    if checker.check_black(event.user_id):
        await matcher.skip()

    return checker.config


def is_number(s: str) -> bool:
    """
    说明:
        检测 s 是否为数字
    参数:
        :param s: 文本
    """
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata

        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


def get_bot() -> Optional[Bot]:
    """
    说明:
        获取 bot 对象
    """
    try:
        return list(nonebot.get_bots().values())[0]
    except IndexError:
        return None


def get_matchers(distinct: bool = False) -> List[Type[Matcher]]:
    """
    说明:
        获取所有matcher
    参数:
        distinct: 去重
    """
    _matchers = []
    temp = []
    for i in matchers.keys():
        for matcher in matchers[i]:
            if distinct and matcher.plugin_name in temp:
                continue
            temp.append(matcher.plugin_name)
            _matchers.append(matcher)
    return _matchers


def get_message_at(data: Union[str, Message]) -> List[int]:
    """
    说明:
        获取消息中所有的 at 对象的 qq
    参数:
        :param data: event.json()
    """
    qq_list = []
    if isinstance(data, str):
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "at":
                qq_list.append(int(msg["data"]["qq"]))
    else:
        for seg in data:
            if seg.type == "at":
                qq_list.append(int(seg.data["qq"]))
    return qq_list


def get_message_img(data: Union[str, Message]) -> List[str]:
    """
    说明:
        获取消息中所有的 图片 的链接
    参数:
        :param data: event.json()
    """
    img_list = []
    if isinstance(data, str):
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "image":
                img_list.append(msg["data"]["url"])
    else:
        for seg in data["image"]:
            img_list.append(seg.data["url"])
    return img_list


def get_message_img_file(data: Union[str, Message]) -> List[str]:
    """
    说明:
        获取消息中所有的 图片file
    参数:
        :param data: event.json()
    """
    file_list = []
    if isinstance(data, str):
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "image":
                file_list.append(msg["data"]["file"])
    else:
        for seg in data["image"]:
            file_list.append(seg.data["file"])
    return file_list


def get_message_text(data: Union[str, Message]) -> str:
    """
    说明:
        获取消息中 纯文本 的信息
    参数:
        :param data: event.json()
    """
    result = ""
    if isinstance(data, str):
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "text":
                result += msg["data"]["text"].strip() + " "
        return result.strip()
    else:
        for seg in data["text"]:
            result += seg.data["text"] + " "
    return result.strip()


def get_message_record(data: Union[str, Message]) -> List[str]:
    """
    说明:
        获取消息中所有 语音 的链接
    参数:
        :param data: event.json()
    """
    record_list = []
    if isinstance(data, str):
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "record":
                record_list.append(msg["data"]["url"])
    else:
        for seg in data["record"]:
            record_list.append(seg.data["url"])
    return record_list


def get_message_json(data: str) -> List[dict]:
    """
    说明:
        获取消息中所有 json
    参数:
        :param data: event.json()
    """
    try:
        json_list = []
        data = json.loads(data)
        for msg in data["message"]:
            if msg["type"] == "json":
                json_list.append(msg["data"])
        return json_list
    except KeyError:
        return []


def is_chinese(word: str) -> bool:
    """
    说明:
        判断字符串是否为纯中文
    参数:
        :param word: 文本
    """
    for ch in word:
        if not "\u4e00" <= ch <= "\u9fff":
            return False
    return True


def insertionBlanks(matched):
    """
    说明:
        re
    """
    return " ".join(matched.group())


def args_split(args: Union[str, Message]) -> list:
    """
    说明:
        分割参数，支持处理 CQ 消息段。
    参数:
        :param args: 带解析的参数，可以是 MessageSegment 或普通字符串
    返回:
        :return list
    """
    args_list = []
    if isinstance(args, Message):
        for i in args:
            if i.type == "at":
                args_list.append(i.data["qq"])
            elif i.type == "text":
                text = re.sub(
                    "[\u4e00-\u9fa5][\d]|[\d][\u4e00-\u9fa5]",
                    insertionBlanks,
                    i.data["text"],
                )
                args_list += text.split()
    else:
        text = re.sub(
            "[\u4e00-\u9fa5][\d]|[\d][\u4e00-\u9fa5]",
            insertionBlanks,
            args,
        )
        args_list = text.split()
    for i in range(len(args_list)):
        if isinstance(args_list[i], int):
            args_list[i] = str(args_list[i])

    return args_list


async def get_user_avatar(qq: int) -> Optional[bytes]:
    """
    说明:
        快捷获取用户头像
    参数:
        :param qq: qq号
    """
    url = f"http://q1.qlogo.cn/g?b=qq&nk={qq}&s=160"
    async with httpx.AsyncClient() as client:
        for _ in range(3):
            try:
                return (await client.get(url)).content
            except TimeoutError:
                pass
    return None


async def get_group_avatar(group_id: int) -> Optional[bytes]:
    """
    说明:
        快捷获取用群头像
    参数:
        :param group_id: 群号
    """
    url = f"http://p.qlogo.cn/gh/{group_id}/{group_id}/640/"
    async with httpx.AsyncClient() as client:
        for _ in range(3):
            try:
                return (await client.get(url)).content
            except TimeoutError:
                pass
    return None
