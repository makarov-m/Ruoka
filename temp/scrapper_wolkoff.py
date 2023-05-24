from datetime import datetime
from bs4 import BeautifulSoup
import requests


# Define a function to scrape the website
def scrape_website():
    url = 'https://wolkoff.fi/ruoka-juoma/#post-1247'

    # Send a request to the website
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the menu items
    menu_items = soup.find_all('li', {'class': 'menu-list__item'})

    # options
    restaurant_name = 'Wolkoff'
    restaurant_website = 'https://wolkoff.fi/ruoka-juoma/#post-1247'
    today = datetime.today()
    #diets = ['L', 'V', 'G', 'M']
    days = ['Maanantai', 'Tiistai', 'Keskiviikko', 'Torstai', 'Perjantai']

    # Loop through the menu items and extract the text from all <p> tags within the divs
    for item in menu_items[:5]:
        menu_day_h4 = item.find_all('h4')
        for elem in menu_day_h4:
            week_day = elem.text
            print(week_day)
        item_texts = item.find_all('p')
        item_strings = [text.get_text(strip=True) for text in item_texts]
        print(item_strings)
        print()
    #     if len(item_strings) > 0:
    #         # this block creates cleans the menu
    #         for count, value in enumerate(item_strings):
    #             menu_day = item_strings[0]
    #             lunch_time = item_strings[1]
    #             value = value.replace("\n", "")
    #             last_four_chars = value[-4:]
    #             if any(i in last_four_chars for i in diets):
    #                 print(f'{menu_day} {lunch_time}, {count}, {value}')

    # pass

scrape_website()