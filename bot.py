import os
import sys
from dotenv import load_dotenv

# Проверка обязательных переменных окружения
required_vars = [
    "BOT_TOKEN",
    "API_ID",
    "API_HASH",
    "SESSION",
    "FOLDER_TITLE",
    "OUTPUT_FILE",
    "GENAI_API_KEY",
]

load_dotenv()
missing = [var for var in required_vars if not os.getenv(var)]
if missing:
    print(f"Error: Missing environment variable(s): {', '.join(missing)}")
    sys.exit(1)

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from main import main

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(
        "Привет! Я бот для парсинга вакансий из Telegram. "
        "Заполни .env и отправь команду /parse с ключевыми словами, чтобы начать."
    )


@dp.message(Command("parse"))
async def parse_command(message: types.Message):
    await message.answer("Парсинг начат...")
    # Extract keywords after the command
    keywords = message.text.split("parse")[1]
    await main(message, keywords)
    await message.answer("Парсинг завершен!")


async def main_bot():
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main_bot())
