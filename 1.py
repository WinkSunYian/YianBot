from utils.http_utils import HTTPClient


http_client = HTTPClient(
    base_url="https://oni-cn.com/solid/",
)


async def TEST():
    query = "algae"
    status, response = await http_client.get(f"{query}")
    print(status, response)


if __name__ == "__main__":
    import asyncio

    async def main():
        await TEST()

    asyncio.run(main())
