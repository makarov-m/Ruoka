#!/usr/bin/env python
import os
import logging
import pandas as pd
import csv
import boto3
import asyncio
from datetime import datetime
from io import StringIO
from dotenv import load_dotenv
from cachetools import TTLCache
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

log = logging.getLogger(__name__)
log.setLevel(os.environ.get('LOGGING_LEVEL', 'INFO').upper())
cache = TTLCache(maxsize=float('inf'), ttl=0.5)

# Initialize bot and dispatcher
load_dotenv()
token = os.getenv('TELEGRAM_LOTTA_TOKEN')
if not token:
    exit("Error: no token provided")
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Keyboard buttons
lang_fi = KeyboardButton('FI')
lang_en = KeyboardButton('EN')
lang_ru = KeyboardButton('RU')
keyboard_lang = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(lang_fi, lang_en, lang_ru)

Wolkoff = KeyboardButton('Wolkoff')
Kitchen = KeyboardButton('Kitchen')
Kehruuhuone = KeyboardButton('Kehruuhuone')
keyboard_rest = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).row(Wolkoff, Kitchen, Kehruuhuone)

# User states
class UserState(StatesGroup):
    language = State()
    restaurant = State()
    stopped = State()

# Middleware for throttling. Ignores any repeated requests for 0.5 sec
class ThrottleMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        if not cache.get(message.chat.id):  # It is assumed that the bot does NOT work in groups
            cache[message.chat.id] = True   # There is no entry in the cache, create
            return
        else:  # skip processing
            raise CancelHandler
        
dp.middleware.setup(ThrottleMiddleware())       

# Read menu function
def read_menu(restaurant: str, lang: str, date: str):
    s3 = boto3.client('s3')
    bucket_name = 'ruokabot'
    object_key = f'{restaurant}.csv'
    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    body = response['Body']
    csv_string = body.read().decode('utf-8')
    df = pd.read_csv(StringIO(csv_string))
    df['Date'] = df['Date'].astype(str)
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m')
    df['Date'] = df['Date'].dt.strftime('%d.%m')
    query_weekday = df[(df["Lang"]==lang)&(df["Date"]==date)]["Weekday"].drop_duplicates()
    query_date = df[(df["Lang"]==lang)&(df["Date"]==date)]["Date"].drop_duplicates()
    query_time = df[(df["Lang"] == lang) & (df["Date"] == date)]["LunchTime"].drop_duplicates()
    query_menu = df[(df["Lang"] == lang) & (df["Date"] == date)]["Menu"].drop_duplicates()
    query_price = df[(df["Lang"] == lang) & (df["Date"] == date)]["Price"].drop_duplicates()
    query_link = df[(df["Lang"] == lang) & (df["Date"] == date)]["MenuLink"].drop_duplicates()
    pd.set_option('display.max_colwidth', None)
    return (
        query_weekday.to_string(index=False), 
        query_date.to_string(index=False), 
        query_time.to_string(index=False), 
        query_menu.to_string(index=False), 
        query_price.to_string(index=False), 
        query_link.to_string(index=False)
        )

# Handlers
@dp.message_handler(commands=['start'], state=UserState.stopped)
async def cmd_start_after_stop(message: types.Message, state: State):
    await message.answer("Bot started. Select Language", reply_markup=keyboard_lang)
    # Set the user state to 'language'
    await UserState.language.set()

@dp.message_handler(commands=['stop'], state="*")
async def cmd_stop(message: types.Message, state: State):
    await message.answer("Bot stopped.")
    # Clear all states and set 'stopped' state
    await state.finish()
    await UserState.stopped.set()

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
    if message.text in ["Wolkoff", "Kitchen", "Kehruuhuone"]:
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

# async def process_event(event, dp: Dispatcher):
#     """
#     Converting an AWS Lambda event to an update and handling that
#     update.
#     """
#     log.debug('Update: ' + str(event))
#     Bot.set_current(dp.bot)
#     update = types.Update.to_object(event)
#     await dp.process_update(update)

# async def main(event):
#     """
#     Asynchronous wrapper for initializing the bot and dispatcher,
#     and launching subsequent functions.
#     """

#     # Bot and dispatcher initialization
#     # bot = Bot(os.environ.get('TELEGRAM_LOTTA_TOKEN'))
#     # storage = MemoryStorage()
#     # dp = Dispatcher(bot, storage=storage)
#     await process_event(event, dp)

#     return 'ok'

# def lambda_handler(event):
#     """AWS Lambda handler."""

#     return asyncio.get_event_loop().run_until_complete(main(event))

