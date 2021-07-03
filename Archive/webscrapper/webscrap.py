import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

URL = 'https://docs.splunksecurityessentials.com/content-detail/'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')
results = soup.find_all('a', href=True)

namelist = []
linkslist = []

description = []
usecase = []
category = []
tactics = []
techniques = []
killchain = []
datasources = []
search = []
searchDesc = []

count = 0
for i, elm in enumerate(results):
    if 'https://docs.splunksecurityessentials.com/content-detail/' in str(elm):
        name = elm.contents[0]
        link = elm['href']
        namelist.append(name)
        linkslist.append(link)


def sublinks(hreflink):
    URL = hreflink
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    body = soup.find("body").find("article").find("div", class_="bookmark_printable_table printable_section")

    description = body.find("p").text
    print(description)

    usecase = body.find("div").find("div").find("h2", text='Use Case').next_sibling

    category = body.find("div").find("div").find("h2", text='Category').next_sibling

    tactics = body.find_all("div")[2].find_all("div", class_="primary mitre_tactic_displayElements")
    tactics = [i.text for i in tactics]

    techniques = body.find_all("div")[2].find_all("div", class_="primary mitre_technique_displayElements")
    techniques = [i.text for i in techniques]

    killchain = body.find_all("div")[2].find_all("div", class_="killchain")
    killchain = [i.text for i in killchain]

    datasources = body.find_all("div")[2].find_all("div", class_="coredatasource")
    datasources = [i.text for i in datasources]

    search = ""
    searchDesc = ""

    try:
        searchTable = body.find("div", class_="donotbreak").find_all("div", class_="donotbreak")[1] \
            .find("table", class_="linebylinespl").find_all("tr")
        for tr in searchTable:
            tds = tr.find_all('td')
            queries = tds[0].text
            desc = tds[1].text
            search = search + queries
            searchDesc = searchDesc + desc
    except IndexError:
        print('<<<<<<<<<<<<<<<<<<<<<<index error')

    return description, usecase, category, tactics, techniques, killchain, datasources, search, searchDesc


for link in tqdm(linkslist):
    print(link)
    a, b, c, d, e, f, g, h, i = sublinks(link)
    description.append(a)
    usecase.append(b)
    category.append(c)
    tactics.append(d)
    techniques.append(e)
    killchain.append(f)
    datasources.append(g)
    search.append(h)
    searchDesc.append(i)

df = pd.DataFrame({
    "title": namelist,
    "description": description,
    "providing_technologies": datasources,
    "category": category,
    "usecase": usecase,
    "mitre_tactics": tactics,
    "mitre_techniques": techniques,
    "killchain": killchain,
    "qualified_search": search,
    "search_steps": search
})

df.to_csv("output.csv", index=False)
