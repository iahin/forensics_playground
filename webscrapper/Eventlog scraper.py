import requests
from bs4 import BeautifulSoup

type = 'no'
eventid = "4661 "

URL = ""
if type == 'sys':
    URL = 'https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventid=9000' + eventid
else:
    URL = 'https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventid=' + eventid

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find('p', class_='hey')
getstring = results.text.strip()

print(getstring)

results = soup.find(
    id="ctl00_ctl00_ctl00_ctl00_Content_Content_Content_Content_FieldsDiv")
results = results.find("ul")
#getstring = results.text.strip()

print(results.text.strip())
