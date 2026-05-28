import pandas as pd
from ddgs import DDGS
import requests
import re
from bs4 import BeautifulSoup
from rapidfuzz import fuzz
import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd

load_dotenv()

client = OpenAI(api_key = os.getenv("API_KEY"))

# JSON data






search_query =[
    "Way Education Pvt Ltd US",
    "Common Foundation Pvt Ltd",
    "Sagip Educational Consultancy Pvt. Ltd",
    "The Next Education Consultancy Pvt. Ltd",
    "Fast Track Education Consultancy Pvt Ltd."
]
path = "data.html"
siteURLName = ""
filteredSiteURLName = ""
webURLName = ""
ScoreBoard = []
best_href = None
best_score = -1


def chat_with_gpt(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# print(chat_with_gpt("Hello GPT-4, how are you?"))

def genWebUrlLinkANDFilteredSiteURL(results):
    count = 0
    dotIndex = 0
    slashIndex = 0
    best_href = None
    best_score = -1
    FBURL = ""
    HrefArr = []
    FilteredHref = []
    

    for i in range(8):
        HrefArr.insert(i,results[i]["href"])

    for i in range(8):
        if "facebook" in HrefArr[i]:
            FBURL = HrefArr[i]
            print("\n")
            print("This is the Facebook LINK ***************")
            print(HrefArr[i])

    FilteredHref = [x for x in HrefArr if not any(k in x for k in ["facebook", "linkedin", "youtube","school","maps","worldwide","tiktok"])]

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

    HrefArr = []
    FilteredHref = []

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

    def core(query):
        name = []
        logo = []
        desc = []
        url = []
        AboutConsultancy = ""
        GPT_DESC = ""

        data = {
            "Name":name,
            "Url":url,
            "Logo":logo,
            "Desc":desc
        }
        
        result = serchQuery(query)

        # JSON name

        name.append(query)


        webUrl = genWebUrlLinkANDFilteredSiteURL(result)

        # JSON url

        url.append(webURLName)

        fetchAndSaveToFile(result,webUrl,path)
        soup = parseHTML(path)
        with open(path,"w",encoding="utf-8"):
            pass
        print("\n")
        print("WEBSITE IMAGE ********************")
        img = soup.find_all("img", alt=re.compile(r"logo|home", re.I))


        if img == []:
            icon = soup.find_all("link",rel="icon")
            print(icon[0]["href"])
            ImgLOGO = icon[0]["href"]

            # JSON LOGO

            logo.append(ImgLOGO)
        else:
            print(img[0]["src"])
            IconLOGO = img[0]["src"]

            # JSON LOGO

            logo.append(IconLOGO)

        description = soup.find_all("p", text = re.compile(r"consultancy|education", re.I))

        print("\n")
        print("WEBSITE DESCRIPTION ********************")

        for desc in description:
            AboutConsultancy = desc.get_text()

        print(AboutConsultancy)

        GPT_DESC = chat_with_gpt(AboutConsultancy + "Summarize the description into 50 words make it clear and professional")

        # JSON DESC

        desc.append(GPT_DESC)

        print("Ending of DESCRIPTION ********************")


        if description == [] or (img == [] and icon == []):
            core(query)

        # JSON Data

        print("############### This is the data to export to json ###############")
        print(data)


   

    for i in range(len(search_query)):
        core(search_query[i])

        

    
    



except Exception as e:
    print("Couldn't scrape Data",e)
