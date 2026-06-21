import asyncio
import logging
import os
import sys

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

load_dotenv()

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()

@dp.message(Command("start", "help"))
async def cmd_start(message: types.Message) -> None:
    await message.answer(
        "Привет! Я бот-список дел.\n\n"
        "Команды:\n"
        "/help - список команд"
    )

async def main() -> None:
    if not TOKEN:
        print("Ошибка: не задан BOT_TOKEN. Смотрите инструкцию в README.")
        sys.exit(1)

    bot = Bot(token=TOKEN)
    print("Бот запущен. Остановка: Ctrl+C")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
