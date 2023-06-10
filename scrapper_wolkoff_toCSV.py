#!/usr/bin/env python
# coding: utf-8
# import codecs
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import deepl
import pandas as pd

# deepl library
auth_key = "ad34c11c-d02c-6496-4ee5-7c52693f6a31:fx"  
translator = deepl.Translator(auth_key)

# Define a function to scrape the website
def scrape_wolkoff():
    url = 'https://wolkoff.fi/ruoka-juoma/#post-1247'

    # Send a request to the website
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the menu items
    menu_items = soup.find_all('li', {'class': 'menu-list__item'})

    # Metadata about restaurant and scrapping
    UpdateDate_value = datetime.today().strftime('%Y-%m-%d %-H:%M:%S %z')
    Restaurant_value = 'Wolkoff'
    LunchTime_value = '11:00-14:00'

    menu_list_fi = []
    menu_list_en = []
    menu_list_ru = []

    # options
    days_FI = []
    days_EN = []
    days_RU = []
    dates_list = []
    counter = 0
    running_date = datetime.today()
    date_object = running_date
    #running_date = '2023-05-22'
    #date_object = datetime.strptime(running_date, '%Y-%m-%d').date()

    # Loop through the menu items and extract the text from all <p> tags within the divs
    for item in menu_items[:5]:
        menu_day_h4 = item.find_all('h4')
        for elem in menu_day_h4:
            week_day_fi = elem.text
            week_day_fi = ''.join([i for i in week_day_fi if not i.isdigit() and i != "." and i != " "])        # exluding dots, numbers and spaces from Weekday
            week_day_en = str(translator.translate_text(f"{week_day_fi}", target_lang="EN-GB"))
            week_day_ru = str(translator.translate_text(f"{week_day_fi}", target_lang="ru"))
            days_FI.append(week_day_fi)
            days_EN.append(week_day_en)
            days_RU.append(week_day_ru)
        item_texts = item.find_all('p')
        item_strings = [text.get_text(strip=True) for text in item_texts if len(text)>0]
        MenuString_FI = [i.replace("\xa0","") for i in item_strings]
        
        # translate 
        MenuString_EN = str(translator.translate_text(f"{MenuString_FI}", target_lang="EN-GB"))
        MenuString_RU = str(translator.translate_text(f"{MenuString_FI}", target_lang="RU"))
        
        # create lists with menu
        menu_list_fi.append(MenuString_FI)
        menu_list_en.append(MenuString_EN)
        menu_list_ru.append(MenuString_RU)
        # working with dates
        WeekDayNumber = date_object.weekday()                 #  Monday = 1, Tuesday = 2 ...
        weekDaysDates = date_object + timedelta(days=counter) #- timedelta(days = WeekDayNumber) 
        day_month = weekDaysDates.strftime('%d.%m')
        dates_list.append(day_month)
        counter = counter + 1
        
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

    df = pd.concat([df_fi, df_en, df_ru])

    df['UpdateDate'] = UpdateDate_value
    df['Restaurant'] = Restaurant_value
    df['LunchTime'] = LunchTime_value
    df['MenuLink'] = url
    df['Price'] = '€14.90/€12.90'
    df = df.reset_index(drop=True)
    
    return df.to_csv(f'{Restaurant_value}.csv')

if __name__ == "__main__":
    scrape_wolkoff()