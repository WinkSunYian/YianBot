# from nonebot import on_command
# from nonebot.adapters.onebot.v11 import (
#     Bot,
#     MessageSegment,
#     MessageEvent,
#     Message
# )
# from nonebot.params import (
#     CommandArg,
# )
# from .data_source import (
#     get_phone,
#     get_qq,
#     get_rand_id,
#     get_id_check,
#     get_qq_price
# )
# from utils.utils import is_number

# __plugin_name__ = 'Query'
# __plugin_usage__ = '查询'

# __plugin_disable_list__ = [
#     "7345222",
#     "488981827",
#     "15656561576"
# ]

# query_number = on_command("#查Q绑", aliases={"#查绑"}, priority=6, block=True)


# @query_number.handle()
# async def query_number_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
#     args_list = str(args).split()
#     """
#     args_list[0] QQ
#     """
#     if len(args_list) != 1 or not is_number(args_list[0]):
#         await query_number.finish(MessageSegment.reply(event.message_id) + "指令用法:\n#查绑 [QQ]\n指令别名:\n查Q绑")
#     elif len(args_list[0]) < 5 or 10 < len(args_list[0]):
#         await query_number.finish(MessageSegment.reply(event.message_id) + "[QQ]的长度应为5-10")
#     elif args_list[0] in __plugin_disable_list__:
#         await query_number.finish(MessageSegment.reply(event.message_id) + "请求错误")
#     else:
#         msg = await get_phone(args_list[0])
#         await query_number.finish(MessageSegment.reply(event.message_id) + msg)


# qq_price = on_command("#QQ估价", aliases={"#估价"}, priority=6, block=True)


# @qq_price.handle()
# async def qq_price_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
#     await qq_price.finish(MessageSegment.reply(event.message_id) + "功能已停用\nps:易封号,停段时间观察")
#     args_list = str(args).split()
#     """
#     args_list[0]: QQ号
#     """
#     if len(args_list) != 1:
#         await qq_price.finish(MessageSegment.reply(event.message_id) + "指令用法:\n#QQ估价 [QQ]\n指令别名:\n估价")
#     elif len(args_list[0]) < 5 or 10 < len(args_list[0]):
#         await qq_price.finish(MessageSegment.reply(event.message_id) + "[QQ]的长度应该为5-10")
#     elif not is_number(args_list[0]):
#         await qq_price.finish(MessageSegment.reply(event.message_id) + "[QQ]只能由数字组成")
#     else:
#         msg = await get_qq_price(args_list[0])
#         await qq_price.finish(MessageSegment.reply(event.message_id) + msg)


# # 优化日期12/25
# # 以下代码未优化

# query_qq = on_command("#Q反查", aliases={"#反查"}, priority=6, block=True)


# @query_qq.handle()
# async def query_qq_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
#     await query_qq.finish(MessageSegment.reply(event.message_id) + "功能已停用\nps:易封号,停段时间观察")
#     args_list = str(args).split()
#     """
#     args_list[0]: 手机号
#     """
#     if len(args_list) != 1:
#         await id_check.finish(MessageSegment.reply(event.message_id) + "指令用法:\n#反查 [手机号]\n指令别名:\nQ反查")
#     elif len(args_list[0]) != 11:
#         await query_qq.finish(MessageSegment.reply(event.message_id) + "[手机号]的长度应该为11")
#     elif args_list[0] in __plugin_disable_list__:
#         await query_number.finish(MessageSegment.reply(event.message_id) + "请求错误")
#     else:
#         msg = await get_qq(args_list[0])
#         await query_qq.finish(MessageSegment.reply(event.message_id) + msg)


# rand_id = on_command("#随机身份证", aliases={"#随机ID"}, priority=6, block=True)


# @rand_id.handle()
# async def rand_id_handle(bot: Bot, event: MessageEvent):
#     await rand_id.finish(MessageSegment.reply(event.message_id) + "功能已停用\nps:易封号,停段时间观察")
#     msg = await get_rand_id()
#     await rand_id.finish(MessageSegment.reply(event.message_id) + msg)


# id_check = on_command("#二要素校验", aliases={"#校验"}, priority=6, block=True)


# @id_check.handle()
# async def id_check_handle(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
#     await id_check.finish(MessageSegment.reply(event.message_id) + "功能已停用\nps:易封号,停段时间观察")
#     args_list = str(args).split()
#     """
#     args_list[0]: 姓名
#     args_list[1.yml]: 身份证号
#     """
#     if len(args_list) != 2:
#         await id_check.finish(
#             MessageSegment.reply(event.message_id) + "指令用法:\n#二要素校验 [姓名] [身份证号]\n指令别名:\n校验")
#     elif len(args_list[1]) != 18:
#         await id_check.finish(MessageSegment.reply(event.message_id) + "[身份证号]的长度应该为18")
#     else:
#         msg = await get_id_check(args_list[0], args_list[1])
#         await id_check.finish(MessageSegment.reply(event.message_id) + msg)
