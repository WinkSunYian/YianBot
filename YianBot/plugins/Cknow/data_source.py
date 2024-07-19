import time
import aiohttp
import json

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9',
    'origin': 'https://so.csdn.net',
    'referer': 'https://so.csdn.net/so/search?spm=1000.2115.3001.4501&q=C%E7%9F%A5%E9%81%93&t=&u=',
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'username': 'weixin_43178406'
}


async def get_cknows_answer(q):
    async with aiohttp.ClientSession() as session:
        try:
            url = f"https://devbit-api.csdn.net:8086/chatgpt/data/proxy?question={q}&uuid={time.time_ns() // 1000000}_2&source=2&version=3&isTest=true"
            resp = await session.get(url, headers=headers)
            html = await resp.text()
            answer = ""
            for data in html.split("data:"):
                try:
                    data = json.loads(data)
                    answer += data["message"]["content"]["parts"][0]
                except:
                    pass
            return answer
        except:
            return "Cknow回复超时"

