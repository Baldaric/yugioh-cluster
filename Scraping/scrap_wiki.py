from bs4 import BeautifulSoup
from selenium import webdriver
import time
import json

driver = webdriver.Chrome()

BaseUrl = "https://yugipedia.com"
CurrentUrl = "https://yugipedia.com/wiki/Category:Cards_by_effect_properties"

ListLinks = []

while True:
    driver.get(CurrentUrl)
    time.sleep(5)
    html = driver.page_source
    page = BeautifulSoup(html, "html.parser")

    Box = page.find("div", {"class": "mw-category"})

    if Box:
        Links = Box.find_all("a")
        for Link in Links:
            name = Link.text
            href = Link.get("href")
            FullLink = f"{BaseUrl}{href}"
            ListLinks.append({"name": name, "url": FullLink})
        
    NextPage = page.find("a", string="next page")

    if NextPage:
        CurrentUrl = f"{BaseUrl}{NextPage.get('href')}"
        print(f"Go to Next Page: {CurrentUrl}\n")
    else:
        print("No more pages, Scrape part 1 complete")
        break

JsonPath = "Scraping/Wiki_category.json"
with open(JsonPath, "w") as file:
    json.dump(ListLinks, file, indent=4)

driver.quit()

print(f"Effect category links saved to {JsonPath}")