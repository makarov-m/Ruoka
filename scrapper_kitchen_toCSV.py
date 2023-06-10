#!/usr/bin/env python
# coding: utf-8

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import deepl
import pandas as pd

# deepl library
auth_key = "ad34c11c-d02c-6496-4ee5-7c52693f6a31:fx" 
translator = deepl.Translator(auth_key)

# Define a function to scrape the website
def scrape_kitchen():
    url = 'https://ravintolakitchen.fi/lounas-2/'

    # Send a request to the website
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the menu items
    menu_items = soup.find_all('div', {'class': 'column column-block'})

    # options
    today = datetime.today()
    diets = ['L', 'V', 'G', 'M']
    UpdateDate_value = datetime.today().strftime('%Y-%m-%d %-H:%M:%S %z')
    Restaurant_value = 'Kitchen'
    LunchTime_value = '10:30-15:00'

    menu_list_fi = []
    menu_list_en = []
    menu_list_ru = []

    LunchTime = []
    days_FI = []
    days_EN = []
    days_RU = []
    dates_list = []

    # Loop through the menu items and extract the text from all <p> tags within the divs
    for item in menu_items:
        item_texts = item.find_all('p')
        item_strings = [text.get_text(strip=True) for text in item_texts]
        if len(item_strings) > 0:
            # this block creates cleans the menu
            for count, value in enumerate(item_strings):
                menu_day_fi = item_strings[0]
                lunch_time = item_strings[1]
                value = value.replace("\n", "")
                last_four_chars = value[-4:]
                if any(i in last_four_chars for i in diets):
                    MenuString_FI = value
                    MenuString_EN = translator.translate_text(f"{MenuString_FI}", target_lang="EN-GB")
                    MenuString_RU = translator.translate_text(f"{MenuString_FI}", target_lang="RU")
                    print(f'{menu_day_fi}, {lunch_time}, {count-1}, {MenuString_FI}')
                    menu_list_fi.append(MenuString_FI)
                    menu_list_en.append(MenuString_EN)
                    menu_list_ru.append(MenuString_RU)
                    Weekday_fi = menu_day_fi.split(" ")[0]
                    Weekday_en = translator.translate_text(f"{Weekday_fi}", target_lang="EN-GB")
                    Weekday_ru = translator.translate_text(f"{Weekday_fi}", target_lang="RU")
                    date = menu_day_fi.split(" ")[1]
                    date = date.split(".")[0]
                    current_datetime = datetime.now()
                    current_month = current_datetime.strftime("%m")
                    # Concatenate the month and day with the separator
                    date_month = date + "." + current_month
                    LunchTime.append(lunch_time)
                    days_FI.append(Weekday_fi)
                    days_EN.append(Weekday_en)
                    days_RU.append(Weekday_ru)
                    dates_list.append(date_month)

    # output from scrapping
    df_fi = pd.DataFrame()
    df_en = pd.DataFrame()
    df_ru = pd.DataFrame()

    df_fi['Date'] = dates_list
    df_en['Date'] = dates_list
    df_ru['Date'] = dates_list

    df_fi['Weekday'] = days_FI
    df_fi['Menu'] = menu_list_fi
    df_fi['Lang'] = "FI"

    df_en['Weekday'] = days_EN
    df_en['Menu'] = menu_list_en
    df_en['Lang'] = "EN"

    df_ru['Weekday'] = days_RU
    df_ru['Menu'] = menu_list_ru
    df_ru['Lang'] = "RU"

    df_fi['LunchTime'] = LunchTime
    df_en['LunchTime'] = LunchTime
    df_ru['LunchTime'] = LunchTime

    df_fi = df_fi.drop_duplicates()
    df_en = df_en.drop_duplicates()
    df_ru = df_ru.drop_duplicates()

    df = pd.concat([df_fi, df_en, df_ru])

    df['UpdateDate'] = UpdateDate_value
    df['Restaurant'] = Restaurant_value
    df['LunchTime'] = LunchTime_value
    df['MenuLink'] = url
    df['Price'] = '€14.90/€11.60'

    df = df.reset_index(drop=True)
    df = df.drop_duplicates()

    return df.to_csv(f'{Restaurant_value}.csv')

if __name__ == "__main__":
    scrape_kitchen()