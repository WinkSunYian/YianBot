import time
import hashlib


def get_luck(user_id):
    data = time.localtime(time.time())[0:3]
    combined_string = f"{data}{user_id}"
    hash_object = hashlib.sha256(combined_string.encode())
    hash_value = int(hash_object.hexdigest(), 16)  
    luck = hash_value % 101 
    
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
