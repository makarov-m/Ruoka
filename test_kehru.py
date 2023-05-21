from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import requests
import json
import deepl

# deepl library
auth_key = "ad34c11c-d02c-6496-4ee5-7c52693f6a31:fx"  # Replace with your key
translator = deepl.Translator(auth_key)

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
    menu_items = soup.find_all('div', {'class': f'sc-b3b37590-7 bqpjRg'})
    print(menu_items)

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
    weekDaysList = ['Maanantai', 'Tiistai', 'Keskiviikko', 'Torstai', 
                    #'Perjantai'
                    ]
    lang = ["FI", "EN", "RU"]
    counter = 0

    # Loop through the menu items and extract the text from all <p> tags within the divs
    for item in menu_items:
        item_texts = item.find_all('span')
        print(item_texts)


if __name__ == "__main__":
    scrape_Kehruuhuone()
    



