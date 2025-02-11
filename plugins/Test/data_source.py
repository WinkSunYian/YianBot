a = {
    "messages": [
        {
            "self_id": 1012896426,
            "user_id": 7345222,
            "time": 1739173806,
            "message_id": 1742426278,
            "message_seq": 1742426278,
            "real_id": 1742426278,
            "message_type": "group",
            "sender": {
                "user_id": 7345222,
                "nickname": "孙先生",
                "card": "大傻逼",
                "role": "admin",
            },
            "raw_message": "我要测试",
            "font": 14,
            "sub_type": "normal",
            "message": [{"type": "text", "data": {"text": "我要测试"}}],
            "message_format": "array",
            "post_type": "message",
            "group_id": 701588207,
        },
        {
            "self_id": 1012896426,
            "user_id": 7345222,
            "time": 1739173834,
            "message_id": 450135087,
            "message_seq": 450135087,
            "real_id": 450135087,
            "message_type": "group",
            "sender": {
                "user_id": 7345222,
                "nickname": "孙先生",
                "card": "大傻逼",
                "role": "admin",
            },
            "raw_message": "#test",
            "font": 14,
            "sub_type": "normal",
            "message": [{"type": "text", "data": {"text": "#test"}}],
            "message_format": "array",
            "post_type": "message",
            "group_id": 701588207,
        },
        {
            "self_id": 1012896426,
            "user_id": 1012896426,
            "time": 1739173834,
            "message_id": 252953718,
            "message_seq": 252953718,
            "real_id": 252953718,
            "message_type": "group",
            "sender": {
                "user_id": 1012896426,
                "nickname": "小逸安",
                "card": "1012896426",
                "role": "member",
            },
            "raw_message": "获取历史记录失败，可能是 API 访问异常。",
            "font": 14,
            "sub_type": "normal",
            "message": [
                {
                    "type": "text",
                    "data": {"text": "获取历史记录失败，可能是 API 访问异常。"},
                }
            ],
            "message_format": "array",
            "post_type": "message_sent",
            "message_sent_type": "self",
            "group_id": 701588207,
        },
        {
            "self_id": 1012896426,
            "user_id": 7345222,
            "time": 1739173902,
            "message_id": 86804741,
            "message_seq": 86804741,
            "real_id": 86804741,
            "message_type": "group",
            "sender": {
                "user_id": 7345222,
                "nickname": "孙先生",
                "card": "大傻逼",
                "role": "admin",
            },
            "raw_message": "#test",
            "font": 14,
            "sub_type": "normal",
            "message": [{"type": "text", "data": {"text": "#test"}}],
            "message_format": "array",
            "post_type": "message",
            "group_id": 701588207,
        },
    ]
}


def to_message_list(data: dict):
    messages = []
    for message in data["messages"]:
        raw_message = (
            message["raw_message"].replace("[CQ:at,qq=1012896426]", "@逸安").strip()
        )
        if message["user_id"] == message["self_id"]:
            messages.append({"role": "assistant", "content": raw_message})
        else:
            messages.append({"role": "user", "content": raw_message})
    return messages


print(to_message_list(a))
