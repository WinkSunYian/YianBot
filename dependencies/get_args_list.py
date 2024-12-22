from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg
from utils.utils import args_split


def get_args_list(args: Message = CommandArg()) -> list:
    return args_split(args)
