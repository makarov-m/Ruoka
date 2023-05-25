import pandas as pd
from datetime import datetime

date = datetime.now().strftime('%d.%m')

def read_menu(restaurant: str, lang: str, date: str):
    df = pd.read_csv(f'{restaurant}.csv')
    df['Date']=df['Date'].astype(str)
    query = df[(df["Lang"]==lang)&(df["Date"]==date)]["Menu"]

    pd.set_option('display.max_colwidth', None)
    print(query.to_string(index=False))

read_menu("Kitchen", "RU", str(date))
