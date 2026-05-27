import pandas as pd
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup

search_query = "Mate's Education Pvt Ltd"

path = "filter.html"

results = DDGS().text(
    query=search_query,
    region = "wt-wt",
    safesearch='off',
    timeLimit='7d',
    max_results=50
)


HrefARR = []
bodrARR =[]
WEBURL = ""
FULLWEBURL = ""
FBBody = ""

for i in range(5):
    HrefARR.insert(i,results[i]["href"])

for i in range(5):
    bodrARR.insert(i,results[i]["body"])



for i in range(5):
    if "facebook" in HrefARR[i]:
        WEBURL = HrefARR[i]


print(WEBURL)

count = 0
slashIndex = 0

for i , c in enumerate(WEBURL):
    if c == "/":
        count +=1
        if count == 3:
            slashIndex = i+1
            break

print(slashIndex)
print(WEBURL[slashIndex:-1])

FULLWEBURL = WEBURL[slashIndex:-1] + ".com"

print(FULLWEBURL)


path = "data.html"

def fetchAndSaveToFile(url,path):
    response = requests.get(url)
    with open(path,"w", encoding="utf-8") as f:
        f.write(response.text)

fetchAndSaveToFile(WEBURL,path)