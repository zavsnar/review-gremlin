import os

from telethon import TelegramClient
from dotenv import load_dotenv

load_dotenv()


async def get_client_with_auth() -> TelegramClient:
    # Replace with your own values from https://my.telegram.org/apps
    API_ID = os.getenv('TELEGRAM_API_ID')
    api_id_int = int(API_ID)
    API_HASH = os.getenv('TELEGRAM_API_HASH')
    PHONE_NUMBER = os.getenv('TELEGRAM_PHONE_NUMBER')
    SESSION_NAME = os.path.abspath(os.path.join(os.path.dirname(__file__), "../telegram_session"))

    telegram_client = TelegramClient(SESSION_NAME, api_id_int, API_HASH)

    await telegram_client.connect()

    if not await telegram_client.is_user_authorized():
        print("First run: Sending code request...")
        await telegram_client.send_code_request(PHONE_NUMBER)
        try:
            code = input('Enter the code you received: ')
            await telegram_client.sign_in(PHONE_NUMBER, code)
        except Exception as e:
            print(f"Failed to sign in: {e}")
            await telegram_client.disconnect()

        print("Signed in successfully!")

    return telegram_client