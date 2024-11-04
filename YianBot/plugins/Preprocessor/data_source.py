from utils.http_utils import http_client


async def get_user_tags_or_create(user_id: int) -> list:
    status, response = await http_client.get(f"/users/{user_id}/tags")
    if response["code"] == 2:
        status, response = await http_client.post(f"/users/{user_id}")
        print(response)


async def get_user_tags(user_id: int) -> list:
    url = "http://bot.sunyian.cloud/api/users/{user_id}/tags"
    headers = {"app-key": "QMCjya2bw60Fh4BMDshA5iQbcZI3l3GM"}
    # response = await Aiohttp(url, method="GET", headers=headers)
    # return response


def is_tag_present(tag_list: list, tag_name: str) -> bool:
    for tag in tag_list:
        if tag.get("tag_name") == tag_name:
            return True
    return False


# 发起一个异步请求
if __name__ == "__main__":
    import asyncio

    asyncio.run(get_user_tags_or_create(100861211))
