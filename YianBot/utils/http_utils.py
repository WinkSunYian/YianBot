import aiohttp


async def Aiohttp(url, method='GET', headers=None, data=None, verify=True, timeout=10) -> str:
    async with aiohttp.ClientSession() as session:
        try:
            if method.upper() == 'POST':
                resp = await session.post(url, headers=headers, data=data, verify_ssl=verify, timeout=timeout)
            else:
                resp = await session.get(url, headers=headers, data=data, verify_ssl=verify, timeout=timeout)
            text = await resp.text()
            return text
        except:
            return ""
