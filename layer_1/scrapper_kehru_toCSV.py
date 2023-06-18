#!/usr/bin/env python
# coding: utf-8
# import codecs
import os
import requests
import pandas as pd
import re
import deepl
import boto3
import csv
from io import StringIO
from lxml import html
from dotenv import load_dotenv
from datetime import datetime

# deepl library
load_dotenv()
translate = os.getenv('TRANSLATE')
if not translate:
    exit("Error: no token provided for deepl")
translator = deepl.Translator(translate)

# aws tokens
load_dotenv()
aws_access_key_id = os.getenv('aws_access_key_id')
aws_secret_access_key = os.getenv('aws_secret_access_key')
if not aws_access_key_id or not aws_secret_access_key:
    exit("Error: no token provided for aws")

def scrape_Kehruuhuone():
    # Request the page
    url = 'https://www.raflaamo.fi/fi/ravintola/lappeenranta/kehruuhuone/menu/lounas?menuGroupId=2026&menuGroupTitle=burgerit'
    page = requests.get(url)
    # Modified XPath to retrieve text content
    Xpath = '//*[@id="__next"]/div[1]/main/div/article/div[3]/div//text()'  
    
    # Parsing the page
    tree = html.fromstring(page.content) 
    
    # Get element text using XPath
    content = tree.xpath(Xpath)

    # Initialize the lists to store the data
    dates = []
    prices = []
            
    # Initialize the dictionary to store the sublists
    day_lists_fi = {'maanantai': [], 'tiistai': [], 'keskiviikko': [], 'torstai': [], 'perjantai': []}
    day_lists_en = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': []}
    day_lists_ru = {'понедельник': [], 'вторник': [], 'среда': [], 'четверг': [], 'пятница': []}

    # Iterate over the data and split it into sublists based on the day of the week
    for item in content:
        if item.strip().lower() in day_lists_fi:
            # Update the current_day variable
            current_day = item.strip().lower()
        elif current_day is not None and not item.isspace():
            # Append the non-empty and non-whitespace item to the corresponding day list
            day_lists_fi[current_day].append(item)

    # extracting dates from webpage
    for key, value in day_lists_fi.items():
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

    # extracting menu from webpage
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
                elif re.match(date_pattern, item):
                    date_format_full = "%d.%m.%Y"
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

    # extract menus from mixed data (time, prices, etc.) in Finnish
    menu_mon_fi = create_menu(day_lists_fi['maanantai'])
    menu_tue_fi = create_menu(day_lists_fi['tiistai'])
    menu_wed_fi = create_menu(day_lists_fi['keskiviikko'])
    menu_thu_fi = create_menu(day_lists_fi['torstai'])
    menu_fri_fi = create_menu(day_lists_fi['perjantai'])
    # translate EN
    menu_mon_en = translator.translate_text(f"{menu_mon_fi}", target_lang="EN-GB")
    menu_tue_en = translator.translate_text(f"{menu_tue_fi}", target_lang="EN-GB")
    menu_wed_en = translator.translate_text(f"{menu_wed_fi}", target_lang="EN-GB")
    menu_thu_en = translator.translate_text(f"{menu_thu_fi}", target_lang="EN-GB")
    menu_fri_en = translator.translate_text(f"{menu_fri_fi}", target_lang="EN-GB")
    # translate RU
    menu_mon_ru = translator.translate_text(f"{menu_mon_fi}", target_lang="RU")
    menu_tue_ru = translator.translate_text(f"{menu_tue_fi}", target_lang="RU")
    menu_wed_ru = translator.translate_text(f"{menu_wed_fi}", target_lang="RU")
    menu_thu_ru = translator.translate_text(f"{menu_thu_fi}", target_lang="RU")
    menu_fri_ru = translator.translate_text(f"{menu_fri_fi}", target_lang="RU")

    # reassign menus to each day
    day_lists_fi['maanantai'] = menu_mon_fi
    day_lists_fi['tiistai'] = menu_tue_fi
    day_lists_fi['keskiviikko'] = menu_wed_fi
    day_lists_fi['torstai'] = menu_thu_fi
    day_lists_fi['perjantai'] = menu_fri_fi

    # reassign menus to each day in english
    day_lists_en['Monday'] = menu_mon_en
    day_lists_en['Tuesday'] = menu_tue_en
    day_lists_en['Wednesday'] = menu_wed_en
    day_lists_en['Thursday'] = menu_thu_en
    day_lists_en['Friday'] = menu_fri_en

    # reassign menus to each day in russian
    day_lists_ru['понедельник'] = menu_mon_ru
    day_lists_ru['вторник'] = menu_tue_ru
    day_lists_ru['среда'] = menu_wed_ru
    day_lists_ru['четверг'] = menu_thu_ru
    day_lists_ru['пятница'] = menu_fri_ru

    # store menus in dataframe
    df_menu_fi = pd.DataFrame([day_lists_fi]).T.reset_index()
    df_menu_fi = df_menu_fi.rename(columns={"index": "Weekday", 0: "Menu"})

    # store menus in dataframe
    df_menu_en = pd.DataFrame([day_lists_en]).T.reset_index()
    df_menu_en = df_menu_en.rename(columns={"index": "Weekday", 0: "Menu"})

    # store menus in dataframe
    df_menu_ru = pd.DataFrame([day_lists_ru]).T.reset_index()
    df_menu_ru = df_menu_ru.rename(columns={"index": "Weekday", 0: "Menu"})

    # creating output dataframe
    df_fi = pd.DataFrame()
    df_en = pd.DataFrame()
    df_ru = pd.DataFrame()

    now = datetime.today().strftime('%Y-%m-%d %-H:%M:%S %z')
    Restaurant_value = "Kehruuhuone"

    df_fi['Date'] = dates
    df_fi['Weekday'] = df_menu_fi['Weekday']
    df_fi['Menu'] = df_menu_fi['Menu']
    df_fi['Lang'] = "FI"
    df_fi['UpdateDate'] = now
    df_fi['Restaurant'] = Restaurant_value
    df_fi['LunchTime'] = '11:00-14:00'
    df_fi['MenuLink'] = url
    df_fi['Price'] = '€14.90/€12.90'

    df_en['Date'] = dates
    df_en['Weekday'] = df_menu_en['Weekday']
    df_en['Menu'] = df_menu_en['Menu']
    df_en['Lang'] = "EN"
    df_en['UpdateDate'] = now
    df_en['Restaurant'] = Restaurant_value
    df_en['LunchTime'] = '11:00-14:00'
    df_en['MenuLink'] = url
    df_en['Price'] = '€14.90/€12.90'

    df_ru['Date'] = dates
    df_ru['Weekday'] = df_menu_ru['Weekday']
    df_ru['Menu'] = df_menu_ru['Menu']
    df_ru['Lang'] = "RU"
    df_ru['UpdateDate'] = now
    df_ru['Restaurant'] = Restaurant_value
    df_ru['LunchTime'] = '11:00-14:00'
    df_ru['MenuLink'] = url
    df_ru['Price'] = '€14.90/€12.90'

    df = pd.concat([df_fi, df_en, df_ru])
    df = df.reset_index(drop=True)
    return df#.to_csv(f'{Restaurant_value}.csv')

if __name__ == "__main__":
    # init session to aws
    # session = boto3.Session(
    #     aws_access_key_id=aws_access_key_id,
    #     aws_secret_access_key=aws_access_key_id
    # )
    # s3 = session.resource('s3')
    s3 = boto3.resource("s3")

    # Convert DataFrame to CSV format in memory
    df = scrape_Kehruuhuone()
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    # Upload CSV file to S3
    bucket_name = 'ruokabot'
    file_name = 'Kehruuhuone.csv'
    s3.Object(bucket_name, file_name).put(Body=csv_buffer.getvalue())

