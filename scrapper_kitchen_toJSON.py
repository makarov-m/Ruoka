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


# Define a function to scrape the website
def scrape_website():
    url = 'https://ravintolakitchen.fi/lounas-2/'

    # Send a request to the website
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the menu items
    menu_items = soup.find_all('div', {'class': 'column column-block'})

    # options
    restaurant_name = 'Kitchen'
    restaurant_website = 'https://ravintolakitchen.fi/'
    today = datetime.today()
    diets = ['L', 'V', 'G', 'M']

    # Loop through the menu items and extract the text from all <p> tags within the divs
    for item in menu_items:
        item_texts = item.find_all('p')
        item_strings = [text.get_text(strip=True) for text in item_texts]
        if len(item_strings) > 0:
            # this block creates cleans the menu
            for count, value in enumerate(item_strings):
                menu_day = item_strings[0]
                lunch_time = item_strings[1]
                value = value.replace("\n", "")
                last_four_chars = value[-4:]
                if any(i in last_four_chars for i in diets):
                    #print(f'{menu_day}, {lunch_time}, {count}, {value}')
                    MenuString_FI = value
                    MenuString_EN = translator.translate_text(f"{MenuString_FI}", target_lang="EN-GB")
                    MenuString_RU = translator.translate_text(f"{MenuString_FI}", target_lang="RU")
                    print(f'{menu_day}, {lunch_time}, {count-1}, {MenuString_RU}')
    
    pass

scrape_website()