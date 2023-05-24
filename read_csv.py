import pandas as pd

def read_menu(restaurant: str, lang: str, date: str):
    df = pd.read_csv(f'{restaurant}.csv')
    df['Date']=df['Date'].astype(str)
    query = df[(df["Lang"]==lang)&(df["Date"]==date)]["Menu"]

    pd.set_option('display.max_colwidth', None)
    print(query.to_string(index=False))

read_menu("Wolkoff", "RU", "22.05")
