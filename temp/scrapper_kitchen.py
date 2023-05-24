from datetime import datetime
from bs4 import BeautifulSoup
import requests


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
                    print(f'{menu_day}, {lunch_time}, {count}, {value}')
    
    pass

scrape_website()