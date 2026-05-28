import pandas as pd
from ddgs import DDGS
import requests
import re
from bs4 import BeautifulSoup
from rapidfuzz import fuzz

search_query =[
    "Mate's Education Pvt Ltd",
    "Brilliant Education And Career Services Pvt. Ltd.",
    "Kangaroo Education Foundation Pvt. Ltd.",
    "Netco Technology Pvt Ltd",
    "Prime Education Information Center Pvt. Ltd",
    "Shatakshee Educational Foundation Pvt Ltd",
    "Oli And Associates Pvt. Ltd.",
    "Himalayan White House Education Consultancy Pvt Ltd.",
    "Way Education Pvt Ltd US",
    "Common Foundation Pvt Ltd",
    "Sagip Educational Consultancy Pvt. Ltd",
    "The Next Education Consultancy Pvt. Ltd",
    "Fast Track Education Consultancy Pvt Ltd.",
    "Wide Range Consultancy Pvt Ltd",
    "Expert Education and Visa Service Nepal Pvt. Ltd",
    "Golden Gate International Education Pvt. Ltd.",
    "Tara International Education Pvt",
    "Open Vision Education Foundation Pvt. Ltd.",
    "Edupark Pvt. Ltd.",
    "Guru The Pathfinderk"
]
path = "data.html"
siteURLName = ""
filteredSiteURLName = ""
webURLName = ""
HrefArr = []
FilteredHref = []
ScoreBoard = []

siteCount = 0



best_href = None
best_score = -1

def genWebUrlLinkANDFilteredSiteURL(results):
    count = 0
    dotIndex = 0
    slashIndex = 0
    best_href = None
    best_score = -1
    FBURL = ""

    for i in range(8):
        HrefArr.insert(i,results[i]["href"])

    for i in range(8):
        if "facebook" in HrefArr[i]:
            FBURL = HrefArr[i]
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

    for i , c in enumerate(FBURL):
        if c == "/":
            count +=1
            if count == 3:
                slashIndex = i+1
                break

    siteURLName = "https://"+FBURL[slashIndex:-1]

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

    return webURLName

    


def serchQuery(queryName):
    return DDGS().text(
    query=queryName,
    region = "wt-wt",
    safesearch='off',
    timeLimit='7d',
    max_results=50
)


def fetchAndSaveToFile(results,url,path):
    response = requests.get(url)
    with open(path,"w", encoding="utf-8") as f:
        f.write(response.text)


def parseHTML(path):
    with open(path,"r", encoding="utf-8") as f:
        html_content = f.read()

        soup = BeautifulSoup(html_content,"html.parser")
        return soup


try:
    
    for i in range(len(search_query)):
        result = serchQuery(search_query[i])
        webUrl = genWebUrlLinkANDFilteredSiteURL(result)
        fetchAndSaveToFile(result,webUrl,path)
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
