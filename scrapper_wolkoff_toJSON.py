#!/usr/bin/env python
# coding: utf-8
# import codecs
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


# Define a function to scrape the website
def scrape_website():
    url = 'https://wolkoff.fi/ruoka-juoma/#post-1247'

    # Send a request to the website
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the menu items
    menu_items = soup.find_all('li', {'class': 'menu-list__item'})

    # Metadata about restaurant and scrapping
    UpdateDate_value = datetime.today().strftime('%Y-%m-%d %-H:%M:%S %z')
    UpdateDate_dict = create_dict('UpdateDate', UpdateDate_value)

    Restaurant_value = 'Wolkoff'
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

    # options
    today = datetime.today()
    diets = ['L', 'V', 'G', 'M']
    lang = ["FI", "EN", "RU"]
    days_FI = []
    days_EN = []
    days_RU = []
    dates_list = []
    counter = 0
    #running_date = datetime.today()
    running_date = '2023-05-22'
    date_object = datetime.strptime(running_date, '%Y-%m-%d').date()

    # Loop through the menu items and extract the text from all <p> tags within the divs
    for item in menu_items[:5]:
        menu_day_h4 = item.find_all('h4')
        for elem in menu_day_h4:
            #print(elem)
            week_day_fi = elem.text
            #print(week_day_fi)
            week_day_fi = ''.join([i for i in week_day_fi if not i.isdigit() and i != "." and i != " "])        # exluding dots, numbers and spaces from Weekday
            #week_day_en = str(translator.translate_text(f"{week_day_fi}", target_lang="EN-GB"))
            #week_day_ru = str(translator.translate_text(f"{week_day_fi}", target_lang="ru"))
            days_FI.append(week_day_fi)
            #days_EN.append(week_day_en)
            #days_RU.append(week_day_ru)
        item_texts = item.find_all('p')
        item_strings = [text.get_text(strip=True) for text in item_texts if len(text)>0]
        MenuString_FI = [i.replace("\xa0","") for i in item_strings]
        #print(MenuString_FI)
        
        # translate 
        #MenuString_EN = str(translator.translate_text(f"{MenuString_FI}", target_lang="EN-GB"))
        #MenuString_RU = str(translator.translate_text(f"{MenuString_FI}", target_lang="RU"))
        
        # create lists with menu
        menu_list_fi.append(MenuString_FI)
        #menu_list_en.append(MenuString_EN)
        #menu_list_ru.append(MenuString_RU)
        # working with dates
        WeekDayNumber = date_object.weekday()          # Monday = 1, Tuesday = 2 ...
        weekDaysDates = date_object + timedelta(days=counter) #- timedelta(days = WeekDayNumber) 
        day_month = weekDaysDates.strftime('%d.%m')
        dates_list.append(day_month)
        counter = counter + 1
    # output from scrapping
    #print(dates_list)
    #print(days_FI)
    # print(days_EN)
    # print(days_RU)
    #print(menu_list_fi)
    # print(menu_list_en)
    # print(menu_list_ru)

    # for i in range(5):
    #     key_fi = days_FI[i]
    #     value_fi = menu_list_fi[i]    
    #     menu_dict_fi[key_fi] = value_fi

    #     key_en = days_EN[i]
    #     value_en = menu_list_en[i]    
    #     menu_dict_en[key_en] = value_en

    #     key_ru = days_RU[i]
    #     value_ru = menu_list_ru[i]    
    #     menu_dict_ru[key_ru] = value_ru

    jsonListFi = []
    for i in range(len(dates_list)):
        jsonListFi.append({f"{str(dates_list[i])}":{"Weekday":days_FI[i], "Menu":menu_list_fi[i]}})
    #print(jsonListFi)

    #menu_dict_fi_key = "FI"
    #menu_dict_fi_value = jsonListFi
    #menu_dict_fi[menu_dict_fi_key] = menu_dict_fi_value
    #menu_dict_fi.append({"FI":jsonListFi})
    #print(menu_dict_fi)
    #print(jsonListFi)
    fi_json_menu = json.dumps(jsonListFi, indent=4)
    print(json.loads(fi_json_menu))
    #read_menu = json.loads(fi_json_menu)
    #print(read_menu)

    #print(menu_dict_fi)
    #print(menu_dict_en)
    #print(menu_dict_ru)

scrape_website()