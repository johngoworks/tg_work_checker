from telethon import TelegramClient
from dotenv import load_dotenv
import os

load_dotenv()
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION = os.environ.get("SESSION")


async def initialize_session():
    if not API_ID or not API_HASH or not SESSION:
        raise ValueError(
            "API_ID, API_HASH, and SESSION must be set in the environment variables."
        )
    client = TelegramClient(SESSION, API_ID, API_HASH)
    await client.start()
    await client.disconnect()
    print("Session initialized successfully.")


if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(initialize_session())
    except Exception as e:
        print(f"An error occurred while initializing the session: {e}")
