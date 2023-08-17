import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardMarkup
from aiogram.types import Message, KeyboardButton

import base


dp = Dispatcher()
bot = Bot(token="ВСТАВЬТЕ СЮДА ВАШ ТОКЕН")

@dp.message(Command("start"))
@dp.message(lambda message: message.text == "start")
async def cmd_start(message: Message):
    await message.answer('Привет! С помощью этого бота ты можешь парсить необходимую страницу сайта https://www.hard-tuning.ru/!👋', reply_markup=ReplyKeyboardMarkup(
        keyboard = [
            [
                KeyboardButton(text='🚩Начать!🚩', resize_keyboard=True)
            ]
        ]
    ))


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(base.router)
    logging.basicConfig(level=logging.INFO)
    try:
        await dp.start_polling(bot)
    except Exception as e:
        # In cases when Telegram Bot API was inaccessible don't need to stop polling
        # process because some developers can't make auto-restarting of the script
        print(f"ERROR : Failed to fetch updates! \n")

if __name__ == "__main__":
    asyncio.run(main())
