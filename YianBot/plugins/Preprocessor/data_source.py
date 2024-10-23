from utils.http_utils import Aiohttp


async def get_user_tags(user_id: int) -> list:
    url = "http://api.sunyian.cloud/get-user-tag-or-register/"
    headers = {"API-Key": "jix8ZqQlAle43JyjDqgpllmO7LOvwzEz"}
    data = {"qq_id": user_id}
    response = await Aiohttp(url, method="POST", headers=headers, json=data)
    return response["data"]["tags"]


def is_tag_present(tag_list: list, tag_name: str) -> bool:
    for tag in tag_list:
        if tag.get("tag_name") == tag_name:
            return True
    return False
