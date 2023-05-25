#!/usr/bin/env python

import logging
import pandas as pd
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from datetime import datetime


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token="6011465609:AAEXd6yBibr1KGZoofKgkM13YeMQ8z_6aHk")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Keyboard buttons
lang_fi = KeyboardButton('FI')
lang_en = KeyboardButton('EN')
lang_ru = KeyboardButton('RU')
keyboard_lang = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(lang_fi, lang_en, lang_ru)

Wolkoff = KeyboardButton('Wolkoff')
Kitchen = KeyboardButton('Kitchen')
keyboard_rest = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(Wolkoff, Kitchen)

# User states
class UserState(StatesGroup):
    language = State()
    restaurant = State()
    stopped = State()


# Read menu function
def read_menu(restaurant: str, lang: str, date: str):
    df = pd.read_csv(f'{restaurant}.csv')
    df['Date']=df['Date'].astype(str)
    query = df[(df["Lang"] == lang) & (df["Date"] == date)]["Menu"]

    pd.set_option('display.max_colwidth', None)
    return query.to_string(index=False)

# Handlers
@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message, state: State):
    if state is None:
        await message.answer("Select Language", reply_markup=keyboard_lang)
        # Set the user state to 'language'
        await UserState.language.set()
    else:
        await message.answer("The bot is already running. You can select a new language or stop the bot.")

@dp.message_handler(commands=['stop'], state="*")
async def cmd_stop(message: types.Message, state: State):
    await message.answer("Bot stopped.")
    # Clear all states and set 'stopped' state
    await state.finish()
    await UserState.stopped.set()

@dp.message_handler(commands=['start'], state=UserState.stopped)
async def cmd_start_after_stop(message: types.Message, state: State):
    await message.answer("Bot started. Select Language", reply_markup=keyboard_lang)
    # Set the user state to 'language'
    await UserState.language.set()

@dp.message_handler(state=UserState.language)
async def process_language(message: types.Message, state: State):
    if message.text in ["FI", "EN", "RU"]:
        await state.update_data(language=message.text)
        await message.answer("Select Restaurant", reply_markup=keyboard_rest)
        # Transition the state from 'language' to 'restaurant'
        await UserState.restaurant.set()
    else:
        await message.answer("Invalid language selection")

@dp.message_handler(state=UserState.restaurant)
async def process_restaurant(message: types.Message, state: State):
    if message.text in ["Wolkoff", "Kitchen"]:
        # Access the user's selected language from state data
        user_data = await state.get_data()
        language = user_data.get('language')

        # Set the date parameter to the current date in the format '%d.%m'
        date = datetime.now().strftime('%d.%m')

        # Call the read_menu function with appropriate arguments
        menu = read_menu(message.text, language, date)

        await message.answer(menu)
    else:
        await message.answer("Invalid restaurant selection")

# Main function
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
