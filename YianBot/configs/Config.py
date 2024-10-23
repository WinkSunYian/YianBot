from nonebot import get_driver
from pydantic import BaseModel, Extra, Field


class BotConfig(BaseModel, extra=Extra.ignore):
    """
    默认配置
    """
    nickname: list[str] = Field(["bot"])
    master: str = Field("10001")
    superusers: list[str] = Field(["10001"])


class TencentCloudConfig(BaseModel, extra=Extra.ignore):
    """
    腾讯云配置
    """
    tencent_bot_id: str = Field("")
    tencent_secret_id: str = Field("")
    tencent_secret_key: str = Field("")


class BaiduCloudConfig(BaseModel, extra=Extra.ignore):
    """
    百度云配置
    """
    baidu_api_key: str = Field("")
    baidu_secret_key: str = Field("")


config = get_driver().config
BotConfig = BotConfig.parse_obj(config)
TencentCloudConfig = TencentCloudConfig.parse_obj(config)
BaiduCloudConfig = BaiduCloudConfig.parse_obj(config)

NICKNAME: str = BotConfig.nickname[0]
MASTER: int = int(BotConfig.master)
