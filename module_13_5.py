from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio
import TokenBot


bot = Bot(token = TokenBot.api)
dp = Dispatcher(bot, storage = MemoryStorage())
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton( text= 'Информация')
button2 = KeyboardButton( text= 'Рассчитать')
kb.row(button, button2)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    activity = State()
    gender = State()

@dp.message_handler(commands =['start'])
async def start_message(message):
    await message.answer("Привет! Я бот помогающий твоему здоровью.", reply_markup = kb)

@dp.message_handler(text =['Информация'])
async def inform(message):
    await message.answer("Информация о боте.")

@dp.message_handler(text =['Рассчитать'])
async def set_age(message):
    await message.answer("Введите свой возраст:")
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer("Введите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_weight(message, state):
    await state.update_data(weight = message.text)
    await message.answer("Выберите свою активность: Минимальная - 1, Слабая - 2 , Средняя - 3, Высокая - 4, Экстра - 5")
    await UserState.activity.set()

@dp.message_handler(state=UserState.activity)
async def set_weight(message, state):
    await state.update_data(activity = message.text)
    await message.answer("Введите свой пол: Мужчина- 1, Женщина - 0  ")
    await UserState.gender.set()

@dp.message_handler(state=UserState.gender)
async def send_calories(message, state):
    await state.update_data(gender=message.text)

    data = await state.get_data()

    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    activity = int(data['activity'])
    gender = float(data['gender'])

    if gender:
        if activity == 1:
            calories = (10 * weight + 6.25 * growth - 5 * age + 5) * 1.2
        elif activity == 2:
            calories = (10 * weight + 6.25 * growth - 5 * age + 5) * 1.375
        elif activity == 3:
            calories = (10 * weight + 6.25 * growth - 5 * age + 5) * 1.55
        elif activity == 4:
            calories = (10 * weight + 6.25 * growth - 5 * age + 5) * 1.725
        else:
            calories = (10 * weight + 6.25 * growth - 5 * age + 5) * 1.9
    else:
        if activity == 1:
            calories = (10 * weight + 6.25 * growth - 5 * age - 161) * 1.2
        elif activity == 2:
            calories = (10 * weight + 6.25 * growth - 5 * age - 161) * 1.375
        elif activity == 3:
            calories = (10 * weight + 6.25 * growth - 5 * age - 161) * 1.55
        elif activity == 4:
            calories = (10 * weight + 6.25 * growth - 5 * age - 161) * 1.725
        else:
            calories = (10 * weight + 6.25 * growth - 5 * age - 161) * 1.9

    await message.answer(f'Ваша норма калорий: {calories:.2f} ккал.')

    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates = True)