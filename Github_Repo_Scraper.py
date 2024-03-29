from bs4 import BeautifulSoup
import requests

data_to_scrape = requests.get("https://github.com/jeevandsouza")
soup = BeautifulSoup(data_to_scrape.text, "html.parser")
repos = soup.findAll("span",attrs={"class":"repo"})
primary_languague = soup.findAll("span", attrs={"itemprop":"programmingLanguage"})

for repo,lang in zip(repos,primary_languague):
    print(repo.text," -> ", lang.text)