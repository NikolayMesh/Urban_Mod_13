from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
import data1


bot = Bot(token = data1.api)
dp = Dispatcher(bot, storage = MemoryStorage())


@dp.message_handler(text =['ss', 'ff'])
async def urban_message(message):
    print("Urban message")
    await message.answer("Привет!")

@dp.message_handler(commands =['start'])
async def start_message(message):
    print("Привет! Я бот помогающий твоему здоровью.")
    await message.answer("Рады видеть Вас у Нас! :) ")

@dp.message_handler()
async def all_message(message):
    print("Введите команду /start, чтобы начать общение.")
    await message.answer(message.text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)

