import pandas as pd
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup

search_query = "mate's education pvt ltd"

results = DDGS().text(
    query=search_query,
    region = "wt-wt",
    safesearch='off',
    timeLimit='7d',
    max_results=50
)

path = "data"

def fetchAndSaveToFile(url,path):
    response = requests.get(url)
    with open(path,"w", encoding="utf-8") as f:
        f.write(response.text)

def parseHTML(path):
    with open(path,"r", encoding="utf-8") as f:
        html_content = f.read()

        soup = BeautifulSoup(html_content,"html.parser")
        return soup

HrefArr = []

for i in range(5):
    HrefArr.insert(i,results[i]["href"])

print(HrefArr)




for i in range(5):
    fetchAndSaveToFile(HrefArr[i],path+str(i+".html"))
    # parseHTML(path)
    soup = parseHTML(path+i+".html")





imgs = soup.find_all("link",rel="icon")

if imgs == "" :
    print("no data found")

    print(imgs)


for img in imgs :
    print(img)
# links = soup.find_all("a")

# for link in links:
#     print(link.get("href"))