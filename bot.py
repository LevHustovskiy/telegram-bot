import asyncio
import logging
import os
import sys

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject

load_dotenv()

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()

tasks: dict[int, list[dict]] = {}

@dp.message(Command("start", "help"))
async def cmd_start(message: types.Message) -> None:
    await message.answer(
        "Привет! Я бот-список дел.\n\n"
        "Команды:\n"
        "/add купить хлеб — добавить задачу\n"
        "/list — показать задачи\n"
        "/done 2 — отметить задачу №2 выполненной\n"
        "/delete 2 — удалить задачу №2\n"
        "/help - список команд"
    )

@dp.message(Command("add"))
async def cmd_add(message: types.Message, command: CommandObject) -> None:
    if not command.args:
        await message.answer("Напишите текст задачи: /add купить хлеб")
        return

    user_tasks = tasks.setdefault(message.from_user.id, [])
    user_tasks.append({"text": command.args.strip(), "done": False})
    await message.answer(f"Добавил задачу №{len(user_tasks)}: {command.args.strip()}")

@dp.message(Command("list"))
async def cmd_list(message: types.Message) -> None:
    user_tasks = tasks.get(message.from_user.id, [])
    if not user_tasks:
        await message.answer("Список пуст. Добавьте задачу: /add текст")
        return

    lines = []
    for i, task in enumerate(user_tasks, start=1):
        mark = "✅" if task["done"] else "🔄"
        lines.append(f"{mark} {i}. {task['text']}")
    await message.answer("\n".join(lines))

@dp.message(Command("done"))
async def cmd_done(message: types.Message, command: CommandObject) -> None:
    user_tasks = tasks.get(message.from_user.id, [])

    if not command.args or not command.args.strip().isdigit():
        await message.answer("Укажите номер задачи: /done 2")
        return

    index = int(command.args.strip())
    if not 1 <= index <= len(user_tasks):
        await message.answer(f"Нет задачи с номером {index}. Посмотрите /list")
        return

    user_tasks[index - 1]["done"] = True
    await message.answer(f"Задача №{index} выполнена 🎉")

@dp.message(Command("delete"))
async def cmd_done(message: types.Message, command: CommandObject) -> None:
    user_tasks = tasks.get(message.from_user.id, [])

    if not command.args or not command.args.strip().isdigit():
        await message.answer("Укажите номер задачи: /done 2")
        return

    index = int(command.args.strip())
    if not 1 <= index <= len(user_tasks):
        await message.answer(f"Нет задачи с номером {index}. Посмотрите /list")
        return

    user_tasks.remove(user_tasks[index - 1])
    await message.answer(f"Задача №{index} удалена ❌")

async def main() -> None:
    if not TOKEN:
        print("Ошибка: не задан BOT_TOKEN. Смотрите инструкцию в README.")
        sys.exit(1)

    bot = Bot(token=TOKEN)
    print("Бот запущен. Остановка: Ctrl+C")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
