import requests
import json

# the url is to pull ygoPro API
url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"

Response = requests.get(url)

if Response.status_code == 200: # if the status code is successful
    Cards = Response.json().get("data", []) # put it inside a variable

    with open("yugioh_cards.json", "w") as f:
        json.dump(Cards, f, indent=4) # export is as Json
    
    print(f"Saved {len(Cards)} cards locally.") # to count how many cards are there
else:
    print("Error fetching data:", Response.status_code) # if the status is not 200