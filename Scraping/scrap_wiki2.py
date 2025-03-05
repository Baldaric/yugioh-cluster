from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import time


driver = webdriver.Chrome()

df = pd.read_json("Scraping/Wiki_category.json")

ListName = []
ListFrame = []
ListRace = []
ListCategoryEffect = []

for index, row in df.iterrows():
    EffectCategory = row['name']
    link = row['url']
    driver.get(link)
    time.sleep(2)

    html = driver.page_source
    page = BeautifulSoup(html, "html.parser")

    tables = page.find_all("table", {"class": "sortable wikitable smwtable card-list card-query-main jquery-tablesorter"})

    for table in tables:
        rows = table.find_all("tr")[1:]
        
        for row in rows:
            columns = row.find_all("td")

            if len(columns) >= 3:
                try:
                    name = columns[0].text.strip() if len(columns) > 0 else None
                    frame = columns[2].text.strip() if len(columns) > 2 else None
                    race = columns[3].text.strip() if len(columns) > 3 else None
                    
                    ListName.append(name)
                    ListFrame.append(frame)
                    ListRace.append(race)
                    ListCategoryEffect.append(EffectCategory)

                except Exception as e:
                    print(f"Skipping row due to error: {e}")

driver.quit()

df_result = pd.DataFrame({
    "Name": ListName,
    "Frame": ListFrame,
    "Race": ListRace,
    "Effect Category": ListCategoryEffect})

df_result.to_csv("Scraping/Yugioh_Cards_Details.csv", index=False)

print("Scraping complete. Data saved to Scraping/Yugioh_Cards_Details.csv")