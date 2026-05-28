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

df = pd.read_excel("C:\\Users\\hp\\Downloads\\consultancy data.xlsx")


# importing columd data from excel file from downloads
search_query = df["Name of Company"].tolist()

path = "data.html"
siteURLName = ""
filteredSiteURLName = ""
webURLName = ""
ScoreBoard = []
best_href = None
best_score = -1
query = ""
isDone = ""
soup = ""
soupData = ""


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
    try:
        response = requests.get(url, timeout=60)
        with open(path,"w", encoding="utf-8") as f:
            f.write(response.text)
        return "Done"
    except requests.exceptions.RequestException as e:
        print(f"Couldn't scrape {url}: {e}")
        return None


def parseHTML(path):
    with open(path,"r", encoding="utf-8") as f:
        html_content = f.read()

        soupData = BeautifulSoup(html_content,"html.parser")
        return soupData



name = []
logo = []
ConsultancyDesc = []
url = []
data = {
"Name":name,
"Url":url,
"Logo":logo,
"Desc":ConsultancyDesc
}
AboutConsultancy = ""
GPT_DESC = ""

def core(query,i):
    try:
        global name, logo, desc, url, data, AboutConsultancy, GPT_DESC,soup
        
        

        
        
        result = serchQuery(query)

        # JSON name

        name.insert(i,query)


        webUrl = genWebUrlLinkANDFilteredSiteURL(result)

        # JSON url

        url.insert(i,webUrl)

        isDone = fetchAndSaveToFile(result,webUrl,path)

        if isDone == "Done":
            soup = parseHTML(path)
            with open(path,"w",encoding="utf-8") as f:
                pass
        print("\n")
        print("WEBSITE IMAGE ********************")
        img = soup.find_all("img", alt=re.compile(r"logo|home|icon|brand", re.I)) or soup.find_all("img", class_=re.compile(r"logo|home|icon|brand", re.I)) or soup.find_all("img",src=re.compile(r"logo",re.I))



        if img == []:
            icon = soup.find_all("link", rel="icon") or soup.find_all("link", class_=re.compile(r"logo|home|icon|brand", re.I))

            if icon:
                print(icon[0]["href"])
                ImgLOGO = icon[0]["href"]

                # JSON LOGO

                logo.insert(i,ImgLOGO)
            
            else:
                logo.insert(i,"")

        else:
            if img:
                print(img[0]["src"])
                IconLOGO = img[0]["src"]

                # JSON LOGO

                logo.insert(i,IconLOGO)
            else:
                logo.insert(i,"")

        description = soup.find_all("p", text = re.compile(r"consultancy|education", re.I))

        print("\n")
        print("WEBSITE DESCRIPTION ********************")

        for desc in description:
            AboutConsultancy = desc.get_text()

        print(AboutConsultancy)

        GPT_DESC = chat_with_gpt(AboutConsultancy + " Summarize the description into 50 words make it clear and professional")

        print("\n")
        print("Chat GPT response ++++++---/-*-*--++*-+*/-+//-+- ********************")
        print(GPT_DESC)

        # JSON DESC

        ConsultancyDesc.insert(i,GPT_DESC )

        print("\n")
        print("Ending of DESCRIPTION ********************")


        if description == [] or (img == [] and icon == []):
            core(query)

        # JSON Data
    except Exception as e:
        print("Couldn't scrape Data",e)
        pass
        
    finally:
        print("\n")
        print("############### This is the data to export to json ###############")
        print(data)

        df = pd.DataFrame(data)

        # Export to JSON
        df.to_json("resultdata.json", orient="records", indent=4)
        


for i, query in enumerate(search_query):
    core(query, i)

        

    
    




