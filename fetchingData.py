import requests
from bs4 import BeautifulSoup


def fetchAndSaveToFile(url,path):
    response = requests.get(url)
    with open(path,"w", encoding="utf-8") as f:
        f.write(response.text)

def parseHTML(path):
    with open(path,"r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content,"html.parser")
    return soup

url = "https://timesofindia.indiatimes.com/"
path = "data/info.html"

fetchAndSaveToFile(url,path)

soup = parseHTML(path)

links = soup.find_all("a")

for link in links:
    print(link.get("href"))


