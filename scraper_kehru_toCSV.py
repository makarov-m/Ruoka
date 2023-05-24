#!/usr/bin/env python
# coding: utf-8

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import json
import deepl

# deepl library
auth_key = "ad34c11c-d02c-6496-4ee5-7c52693f6a31:fx"  # Replace with your key
translator = deepl.Translator(auth_key)

# create an empty JSON file named 'json_name.json'
def create_empty_json(json_name):
    with open(f'{json_name}.json', 'w') as f:
        json.dump({}, f)

# create an empty JSON file named 'json_name.json'
def truncate_json(json_name):
    with open(f'{json_name}.json', 'r+') as f:
        f.truncate(0)

def write_json(json_name, dict):
    # load the existing JSON data from the file
    with open(f'{json_name}.json', 'r') as f:
        data = json.load(f)

    # add a dictionary to the data
    data.update(dict)

    # write the modified data back to the file
    with open(f'{json_name}.json', 'w') as f:
        json.dump(data, f)

def create_dict(dict_name: str, value_input):
    # create small dict
    dict = {}
    key = dict_name
    value = value_input
    dict[key] = value
    return dict


# Define a function to scrape the Kehruuhuone
def scrape_Kehruuhuone():
    url = 'https://www.raflaamo.fi/fi/ravintola/lappeenranta/kehruuhuone/menu/lounas?menuGroupId=2026&menuGroupTitle=burgerit'

    # Send a request to the website
    response = requests.get(url)


    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # week number
    week_number = int(datetime.today().strftime('%W'))

    # Extract the menu items
    #menu_items = soup.find_all('div', {'class': f'sc-b3b37590-{week_number}'})
    menu_items = soup.find_all('div', {'class': f'sc-dbbdc76b-15 bBAJkn'})
    #print(menu_items)

    # Metadata about restaurant and scrapping
    UpdateDate_value = datetime.today().strftime('%Y-%m-%d %-H:%M:%S %z')
    UpdateDate_dict = create_dict('UpdateDate', UpdateDate_value)

    Restaurant_value = 'Kehruuhuone'
    Restaurant_dict = create_dict('Restaurant', Restaurant_value)

    LunchTime_value = '11:00-14:00'
    LunchTime_dict = create_dict("LunchTime", LunchTime_value)

    MenuLink_value = url
    MenuLink_dict = create_dict("MenuLink", MenuLink_value)

    menu_dict = {}    

    menu_list_fi = []
    menu_list_en = []
    menu_list_ru = []

    menu_dict_fi = {}
    menu_dict_en = {}
    menu_dict_ru = {}

    weekDaysDatesList = []
    weekDaysList = ['Maanantai', 'Tiistai', 'Keskiviikko', 'Torstai', 'Perjantai']
    lang = ["FI", "EN", "RU"]
    counter = 0

    # Loop through the menu items and extract the text from all <p> tags within the divs
    # for item in menu_items:
    #     item_texts = item.find_all('span')
    #     print(item_texts)
        #MenuString_FI = [text.get_text(strip=True) for text in item_texts]
        #print(MenuString_FI)
        #  MenuString_EN = translator.translate_text(f"{MenuString_FI}", target_lang="EN-GB")
        #  MenuString_RU = translator.translate_text(f"{MenuString_FI}", target_lang="RU")
        #menu_list_fi.append(MenuString_FI)
        #  menu_list_en.append(MenuString_EN)
        #  menu_list_ru.append(MenuString_RU)
        #  WeekDayNumber = datetime.today().weekday()
        #  weekDaysDates = datetime.today() - timedelta(days = WeekDayNumber) + timedelta(days=counter)
        #  day_month = weekDaysDates.strftime('%d.%m')
        #  weekDaysDatesList.append(day_month)
         #print(Restaurant_value)
         #print(weekDaysList[counter])
         #print(MenuString_FI)
         #print()
        #  counter += 1

    # creating dictionaries with menu (external and internal)
    # for i in range(5):
    #     key_ext = weekDaysList[i] + "_" + weekDaysDatesList[i]
        # for j in lang:
        #     key_int = j
        #     value_fi = menu_list_fi[i]
        #     value_en = menu_list_en[i]
        #     value_ru = menu_list_ru[i]

        #     menu_dict_fi[key_int] = value_fi
        #     menu_dict_en[key_int] = value_en
        #     menu_dict_ru[key_int] = value_ru

        # menu_dict[key_ext] = menu_dict_fi
        # menu_dict[key_ext] = menu_dict_en
        # menu_dict[key_ext] = menu_dict_ru
        # value_ru = menu_list_ru[i]
        # menu_dict[key_ext] = value_ru

    
    # print(menu_dict)

    # write the data to JSON
    # create_empty_json(Restaurant_value)
    # write_json(Restaurant_value, UpdateDate_dict)
    # write_json(Restaurant_value, Restaurant_dict)
    # write_json(Restaurant_value, LunchTime_dict)
    # write_json(Restaurant_value, MenuLink_dict)
    # write_json(Restaurant_value, menu_dict)

if __name__ == "__main__":
    scrape_Kehruuhuone()
    



