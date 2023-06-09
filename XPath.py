# Import required modules
from lxml import html
import requests
import pandas as pd
from datetime import datetime, timedelta
import re
 
# Request the page
url = 'https://www.raflaamo.fi/fi/ravintola/lappeenranta/kehruuhuone/menu/lounas?menuGroupId=2026&menuGroupTitle=burgerit'
page = requests.get(url)
Xpath = '//*[@id="__next"]/div[1]/main/div/article/div[3]/div//text()'  # Modified XPath to retrieve text content
 
# Parsing the page
tree = html.fromstring(page.content) 
 
# Get element text using XPath
content = tree.xpath(Xpath)

# Initialize the lists to store the data
dates = []
lounas_times = []
# menus = []
prices = []


# Iterate over the data and extract the required information
# for index, item in enumerate(content):
#     if item != " ":
#         #print(item)
#         date_pattern = r"(\d{1,2}\.\d{1,2}\.)"
#         if item.startswith('Lounas:'):
#             # Update current_lounas_time
#             current_lounas_time = item.replace('Lounas: ', '')
#             current_lounas_time = current_lounas_time.replace('.', '')
#             current_lounas_time = current_lounas_time.replace(' ', '')
#             #print(current_lounas_time)
#         elif item in ["maanantai","tiistai", "keskiviikko", "torstai", "perjantai"]:
#             day_of_week = item
#             #print(day_of_week)
#         elif re.match(date_pattern, item):
#             date_format_full = "%d.%m.%Y"
#             date_format_short = "%d.%m."
#             current_datetime = datetime.now()
#             current_year = current_datetime.strftime("%Y")
#             current_date_full = datetime.strptime(item+current_year, date_format_full)
#             current_date_month = current_date_full.strftime("%d.%m")
#             #print(current_date_month)
#         elif item.endswith('€'):
#             # Update current_menu and current_price
#             current_price = item
#             #print(current_price)
#         elif len(item)>2:
#             current_menu = item
#             #print(current_menu)
#         else:
#             pass
        
# Initialize the dictionary to store the sublists
day_lists = {'maanantai': [], 'tiistai': [], 'keskiviikko': [], 'torstai': [], 'perjantai': []}

# Iterate over the data and split it into sublists based on the day of the week
for item in content:
    if item.strip().lower() in day_lists:
        # Update the current_day variable
        current_day = item.strip().lower()
    elif current_day is not None and not item.isspace():
        # Append the non-empty and non-whitespace item to the corresponding day list
        day_lists[current_day].append(item)

for key, value in day_lists.items():
    if len(value) == 0:
        dates.append(None)
    else:
        for i in value:
            date_pattern = r"(\d{1,2}\.\d{1,2}\.)"
            if re.match(date_pattern, i):
                date_format_full = "%d.%m.%Y"
                date_format_short = "%d.%m."
                current_datetime = datetime.now()
                current_year = current_datetime.strftime("%Y")
                current_date_full = datetime.strptime(i+current_year, date_format_full)
                current_date_month = current_date_full.strftime("%d.%m")
                dates.append(current_date_month)

def create_menu(list):
    menus = []
    for item in list:
        if item != " ":
            date_pattern = r"(\d{1,2}\.\d{1,2}\.)"
            if item.startswith('Lounas:'):
                # Update current_lounas_time
                current_lounas_time = item.replace('Lounas: ', '')
                current_lounas_time = current_lounas_time.replace('.', '')
                current_lounas_time = current_lounas_time.replace(' ', '')
            # elif item in ["maanantai","tiistai", "keskiviikko", "torstai", "perjantai"]:
            #     day_of_week = item
            elif re.match(date_pattern, item):
                date_format_full = "%d.%m.%Y"
                date_format_short = "%d.%m."
                current_datetime = datetime.now()
                current_year = current_datetime.strftime("%Y")
                current_date_full = datetime.strptime(item+current_year, date_format_full)
                current_date_month = current_date_full.strftime("%d.%m")
            elif item.endswith('€'):
                # Update current_menu and current_price
                current_price = item
                prices.append(current_price)
            elif len(item)>3:
                current_menu = item
                menus.append(current_menu)
            else:
                pass
    return menus

menu_mon = create_menu(day_lists['maanantai'])
menu_tue = create_menu(day_lists['tiistai'])
menu_wed = create_menu(day_lists['keskiviikko'])
menu_thu = create_menu(day_lists['torstai'])
menu_fri = create_menu(day_lists['perjantai'])

day_lists['maanantai'] = menu_mon
day_lists['tiistai'] = menu_tue
day_lists['keskiviikko'] = menu_wed
day_lists['torstai'] = menu_thu
day_lists['perjantai'] = menu_fri

df_menu = pd.DataFrame([day_lists]).T.reset_index()
df_menu = df_menu.rename(columns={"index": "Weekday", 0: "Menu"})

df = pd.DataFrame()
#list_weekday = ["maanantai","tiistai", "keskiviikko", "torstai", "perjantai"]
df['Date'] = dates
df['Weekday'] = df_menu['Weekday']
df['Menu'] = df_menu['Menu']

#print(df_menu)
#print()
#print(day_lists)
#print()
#print(dates)
print()
print(df)