import websockets


async def get_chatgpt_answer(q):
    url = 'ws://185.245.41.45:9002'
    try:
        async with websockets.connect(url) as websocket:
            await websocket.send(q)
            recv_text = await websocket.recv()
            return recv_text.strip()
    except TimeoutError:
        return "ChatGPT回复超时"
