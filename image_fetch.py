import requests
import os
import json

# Load the dataset
with open("yugioh_cards.json", "r") as file:
    df = json.load(file)

# Folder to store images
image_folder = "yugioh_images"
os.makedirs(image_folder, exist_ok=True)

def fetch_and_save_image(card_id, image_url):
    """Fetch and save the card image."""
    if image_url:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            image_path = os.path.join(image_folder, f"{card_id}.jpg")
            with open(image_path, "wb") as img_file:
                for chunk in response.iter_content(1024):
                    img_file.write(chunk)
            return image_path
    return None

# Process each card
df_with_images = []
for card in df:
    if "card_images" in card and len(card["card_images"]) > 0:
        image_url = card["card_images"][0]["image_url"]
        image_path = fetch_and_save_image(card["id"], image_url)
        card["local_image_path"] = image_path
    df_with_images.append(card)

# Save results in the folder
output_folder = "yugioh_data"
os.makedirs(output_folder, exist_ok=True)
output_path = os.path.join(output_folder, "yugioh_with_images.json")

with open(output_path, "w") as file:
    json.dump(df_with_images, file, indent=4)

print(f"Images downloaded and metadata saved to {output_path}")