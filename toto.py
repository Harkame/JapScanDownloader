import cloudscraper
import sys
from bs4 import BeautifulSoup

scraper = cloudscraper.create_scraper()

page_url = 'https://www.japscan.to/lecture-en-ligne/hajime-no-ippo/1255/1.html'

page = BeautifulSoup(scraper.get(page_url).content, features='lxml')

with open("output1.html", "w") as file:
    file.write(str(page))
