import time
from random import randint


def get_luck(user_id):
    data = time.localtime(time.time())[0:3]
    luck = user_id // data[2]
    luck = luck % data[0]
    luck = (luck * data[1]) // 10
    luck = luck % 101

    if luck == 0:
        msg = f"您今天的幸运指数为:{luck}\n{'找个地埋了吧'}"
    elif luck < 10:
        msg = f"您今天的幸运指数为:{luck}\n{'个位数,别出门了'}"
    elif luck < 20:
        msg = f"您今天的幸运指数为:{luck}\n{'比个位数好不到哪去'}"
    elif luck < 60:
        msg = f"您今天的幸运指数为:{luck}\n{'不会有人运势不及格吧'}"
    elif luck < 70:
        msg = f"您今天的幸运指数为:{luck}\n{'勉强及格罢了'}"
    elif luck < 90:
        msg = f"您今天的幸运指数为:{luck}\n{'还不错'}"
    elif luck < 100:
        msg = f"您今天的幸运指数为:{luck}\n{'去买彩票'}"
    else:
        msg = f"您今天的幸运指数为:{luck}\n{'天选之人!'}"

    return msg
