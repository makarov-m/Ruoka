# Import the functions from the function files
from scrapper_kehru_toCSV import scrape_Kehruuhuone
from scrapper_kitchen_toCSV import scrape_kitchen
from scrapper_wolkoff_toCSV import scrape_wolkoff

def lambda_handler(event, context):
    # Run the functions
    try:
        scrape_Kehruuhuone()
        print("Kehruuhuome - ok")
        scrape_kitchen()
        print("Kitchen - ok")
        scrape_wolkoff()
        print("Wolkoff - ok")
    except:
        print("smth went wrong - error")
    return print("execution finished")