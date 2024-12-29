# import json
# from utils.http_utils import Aiohttp


# def convert(number):
#     figure = ("零", "一", "二", "三", "四", "五", "六", "七", "八", "九")
#     big_number = ""
#     for i in number:
#         big_number += figure[int(i)]
#     return big_number


# # https://zy.xywlapi.cc/
# async def get_phone(qq):
#     url = f"https://zy.xywlapi.cc/qqapi?qq={qq}"
#     try:
#         html = await Aiohttp(url)
#         data = json.loads(html)
#         if data["message"] == "查询成功":
#             number = data["phone"]
#             msg = "神奇数字：{}\n神奇号码：{}".format(convert(qq), convert(number))
#         else:
#             msg = "找不到呢"
#     except:
#         msg = "逸安刚刚有点走神了,过会再来让我帮您找吧"
#     return msg


# async def get_qq(number):
#     url = f"http://tfapi.top/API/sjfc.php?msg={number}"
#     try:
#         html = get(url, timeout=2).text
#         data = html.split()
#         if data[0].find("成功") != -1:
#             qq = data[2].replace("QQ:", "")
#             msg = "神奇数字: {}\n神奇号码: {}".format(convert(qq), convert(number))
#         else:
#             msg = "找不到呢"
#     except:
#         msg = "逸安刚刚有点走神了,过会再来让我帮您找吧"
#     return msg


# async def get_id_check(name, id):
#     url = f"https://zj.v.api.aa1.cn/api/eys/?name={name}&card={id}"
#     try:
#         html = get(url, timeout=2).text
#         if html.find("正确") != -1:
#             msg = "校验正确"
#         else:
#             msg = "校验错误"
#     except:
#         msg = "逸安刚刚有点走神了,过会再来让我帮您校验吧"
#     return msg


# async def get_rand_id():
#     url = "http://tfapi.top/API/sjsfz.php"
#     try:
#         html = get(url, timeout=2).text
#         msg = html
#     except:
#         msg = "逸安刚刚有点走神了,过会再来让我帮您找吧"
#     return msg


# async def get_qq_price(qq):
#     url = f"https://v.api.aa1.cn/api/qqgj-v2/?qq={qq}"
#     try:
#         html = get(url, timeout=2).text
#         data = json.loads(html)
#         data['gl'] = "杂" if data['gl'] == "" else data['gl']
#         if data["code"] == 200:
#             msg = f"号码: {data['qq']}\n价值: {data['money']}\n类型: {data['gl']}\n位数: {data['ws']}"
#         else:
#             msg = "查询失败"
#     except:
#         msg = "逸安大脑过载,过会再来让我帮估价吧"
#     return msg
