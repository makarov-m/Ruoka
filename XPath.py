# Import required modules
from lxml import html
import requests
 
# Request the page
url = 'https://www.raflaamo.fi/fi/ravintola/lappeenranta/kehruuhuone/menu/lounas?menuGroupId=2026&menuGroupTitle=burgerit'
page = requests.get(url)
Xpath = '//*[@id="__next"]/div[1]/main/div/article/div[3]/div//text()'  # Modified XPath to retrieve text content
 
# Parsing the page
tree = html.fromstring(page.content) 
 
# Get element text using XPath
content = tree.xpath(Xpath)
#full_content = '|'.join(content).strip()  # Join and strip the retrieved text content
 
print(content)
