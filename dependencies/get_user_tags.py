from nonebot.adapters.onebot.v11 import MessageEvent
from utils.http_utils import http_client


async def get_user_tags(event: MessageEvent) -> list:
    return await get_user_tags_or_create_user(event.user_id)


async def get_user_tags_or_create_user(user_id: int) -> list:
    status, response = await http_client.get(f"/users/{user_id}/tags")
    if response["status_code"] == 404:
        status, response = await http_client.post(f"/users/{user_id}")
        return []
    return response["data"]
