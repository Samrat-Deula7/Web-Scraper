import pandas as pd
from ddgs import DDGS
import requests
from bs4 import BeautifulSoup

search_query = "mate's education pvt ltd"

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
FBURL = ""
FBBody = ""

# for i in range(5):
#     obj = {
#     "href": results[i]["href"],
#     "title": results[i]["title"]
#     }
#     titles.insert(i,obj)

for i in range(5):
    HrefARR.insert(i,results[i]["href"])

for i in range(5):
    bodrARR.insert(i,results[i]["body"])



for i in range(5):
    if "facebook" in HrefARR[i]:
        FBURL = HrefARR[i]
        

print(FBURL)


# print(titles[0]["href"])
# response = ""

# for i in range(5):
#     print("Inside the condition"+titles[i]["title"])
#     if "facebook" in titles[i]["title"]:
#         print("Inside the condition"+titles[i]["href"])
#         response = requests.get(titles[i]["href"])
#         print(response)

# with open(path,"w", encoding="utf-8") as f:
#     f.write(response.text)

# print(response)

# print(titles)

# print(results)

# with open(path,"w", encoding="utf-8") as f:
#     f.write(results.text)
