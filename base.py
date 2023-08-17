import asyncio
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from sait_parser import start_parse

router = Router()

class to_parse(StatesGroup):
    web_sait = State()
    to_parse = State()

@router.message(lambda message: message.text == "🔁Начать заново🔁")
@router.message(lambda message: message.text == "🚩Начать!🚩")
async def start_anket(message: Message, state: FSMContext):
    await state.set_state(to_parse.web_sait)
    await message.answer('Пожалуйста, введите необходимую ссылку, по формату: https://www.hard-tuning.ru/catalog/auto/tuning-марка/tuning-модель/ \nНапример https://www.hard-tuning.ru/catalog/auto/tuning-audi/tuning-audi-a3/', reply_markup=ReplyKeyboardRemove())

@router.message(to_parse.web_sait)
async def know_anket(message: Message, state: FSMContext):
    await state.update_data(sait=message.text)
    user_data = await state.get_data()
    link = user_data['sait']
    print(link)
    await state.clear()
    await message.answer(f'Начинаем парсинг ссылки...')
    await start_parse(link, message)