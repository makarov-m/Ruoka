import pandas as pd
from datetime import datetime

date = datetime.now().strftime('%d.%m')
#date = "09.06"

def read_menu(restaurant: str, lang: str, date: str):
    df = pd.read_csv(f'{restaurant}.csv')
    df['Date'] = df['Date'].astype(str)
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m')
    df['Date'] = df['Date'].dt.strftime('%d.%m')
    query_menu = df[(df["Lang"]==lang)&(df["Date"]==date)]["Menu"]
    pd.set_option('display.max_colwidth', None)
    print(query_menu.to_string(index=False))

#read_menu("Wolkoff", "RU", str(date))

def print_date(restaurant: str, lang: str, date: str):
    df = pd.read_csv(f'{restaurant}.csv')
    df['Date'] = df['Date'].astype(str)
    df['Date'] = pd.to_datetime(df['Date'], format='%d.%m')
    df['Date'] = df['Date'].dt.strftime('%d.%m')
    query_date = df[(df["Lang"]==lang)&(df["Date"]==date)]["Date"]
    query_weekday = df[(df["Lang"]==lang)&(df["Date"]==date)]["Weekday"]
    pd.set_option('display.max_colwidth', None)
    print(query_weekday.to_string(index=False), query_date.to_string(index=False))

print_date("Wolkoff", "RU", str(date))