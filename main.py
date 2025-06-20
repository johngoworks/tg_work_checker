from vacancy_parcer import start_parce_vacancies
from aiogram import types
from prompt_sort import start_sort_vacancies
import asyncio
import pprint
import os
import sys


async def main(message_bot: types.Message, sort_filter=None):
    # Step 1: Parse unread messages from Telegram
    messages_to_sort = await start_parce_vacancies(message_bot)

    if not sort_filter:
        sort_filter = input("Ключевые слова: ")  # Example filter, can be modified
    sorted_vacancies = start_sort_vacancies(messages_to_sort, sort_filter)

    with open("result.txt", "w", encoding="utf-8") as f:
        for vacancy in sorted_vacancies:
            f.write(f"{dict(vacancy)}\n")
            vacatcy_text = f'<b>Вакансия:</b> \n   {vacancy.position }\n<b>Зарплата:</b>\n   {vacancy.salary}\n<b>Краткое описание:</b>\n   {vacancy.short_description}\n\n<b>Требования:</b>\n    {vacancy.requirements}\n<b>Условия:</b>\n    {vacancy.conditions}\n<b>Ссылка:</b>\n   <a href="{vacancy.message_link}">перейти</a>\n\n'
            await message_bot.answer(vacatcy_text, parse_mode="HTML")


if __name__ == "__main__":
    required_vars = [
        "BOT_TOKEN",
        "API_ID",
        "API_HASH",
        "SESSION",
        "FOLDER_TITLE",
        "OUTPUT_FILE",
        "GENAI_API_KEY",
    ]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        print(f"Error: Missing environment variable(s): {', '.join(missing)}")
        sys.exit(1)
    asyncio.run(main())
