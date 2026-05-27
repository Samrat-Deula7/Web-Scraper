import pandas as pd
from ddgs import DDGS
import requests
import re
from bs4 import BeautifulSoup
from rapidfuzz import fuzz


search_query = "THE RED EDUHOUSE PVT. LTD."
WEBURL = ""
siteURLName = ""
filteredSiteURLName = ""
webURLName = ""
HrefArr = []
FilteredHref = []
ScoreBoard = []
count = 0
siteCount = 0
slashIndex = 0
dotIndex = 0

best_href = None
best_score = -1

results = DDGS().text(
    query=search_query,
    region = "wt-wt",
    safesearch='off',
    timeLimit='7d',
    max_results=50
)

path = "data.html"

def fetchAndSaveToFile(url,path):
    response = requests.get(url)
    with open(path,"w", encoding="utf-8") as f:
        f.write(response.text)

def parseHTML(path):
    with open(path,"r", encoding="utf-8") as f:
        html_content = f.read()

        soup = BeautifulSoup(html_content,"html.parser")
        return soup


for i in range(8):
    HrefArr.insert(i,results[i]["href"])

for i in range(8):
    if "facebook" in HrefArr[i]:
        WEBURL = HrefArr[i]
        print("\n")
        print("This is the Facebook LINK ***************")
        print(HrefArr[i])


FilteredHref = [x for x in HrefArr if not any(k in x for k in ["facebook", "linkedin", "youtube","school","maps","worldwide"])]

print("\n")
print("ORIGINAL LIST OF LINKS ********************")
print(HrefArr)

print("\n")
print("FILTERED LIST OF LINKS ********************")
print(FilteredHref)

for i , c in enumerate(WEBURL):
    if c == "/":
        count +=1
        if count == 3:
            slashIndex = i+1
            break



siteURLName = "https://"+WEBURL[slashIndex:-1]

if "." in siteURLName:
    for i , s in enumerate(siteURLName):
        if s == ".":
            dotIndex = i
            break

filteredSiteURLName = "https://"+siteURLName[0:dotIndex]

if "edu" in FilteredHref:
    print("\n")
    print("##### adding edu #########")
    filteredSiteURLName +="edu"


print("\n")
print("ORIGINAL SITE NAME ********************")
print(siteURLName)

print("\n")
print("FILTERED SITE NAME ********************")
print(filteredSiteURLName)

if (filteredSiteURLName == "https://"):
    for href in FilteredHref:
        clean_href = href.lower().replace("-", "").replace(" ", "")
        score=fuzz.partial_ratio(siteURLName.lower(),clean_href.lower())
        ScoreBoard.append(score)

        if score > best_score:
            best_score = score
            best_href = href

        webURLName = best_href
else:
    for href in FilteredHref:
        clean_href = href.lower().replace("-", "").replace(" ", "")
        score=fuzz.partial_ratio(filteredSiteURLName.lower(),clean_href.lower())
        ScoreBoard.append(score)

        if score > best_score:
            best_score = score
            best_href = href

        webURLName = best_href


print("\n")
print("WEBSITE URL ********************")
print(webURLName)


try:
    fetchAndSaveToFile(webURLName,path)

    soup = parseHTML(path)
    with open(path,"w",encoding="utf-8"):
        pass


    print("\n")
    print("WEBSITE IMAGE ********************")
    img = soup.find_all("img", alt=re.compile(r"logo|home", re.I))
    print(img)

    if img == []:
        icon = soup.find_all("link",rel="icon")
        print(icon)


    description = soup.find_all("p")

    print("\n")
    print("WEBSITE DESCRIPTION ********************")
    print(description)

except Exception as e:
    print("Couldn't scrape Data",e)