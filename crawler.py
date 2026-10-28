# This script crawls this website "" and saves the data into csv file
import requests
from bs4 import BeautifulSoup

from tqdm import tqdm

import pandas as pd


global_headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


main_page_response = requests.get("https://www.simplyrecipes.com/dinner-recipes-5091433", headers=global_headers)

def get_recipes_links(page):
    html = page.text
    soup = BeautifulSoup(html, "html.parser")
    all_links = soup.find_all("a")
    recipes_links = []
    for link in all_links:
        if link.find_all("img"):
            recipes_links.append(link["href"])
    return recipes_links

def get_recipe(link):
    recipe_page_response = requests.get(link, headers=global_headers)
    soup = BeautifulSoup(recipe_page_response.text, "html.parser")
    recipe_name = soup.find("h1", class_ = "article-heading text-headline-400").get_text()
    recipe_text = ''
    for division in soup.find_all("div"):
        paragraphs = division.find_all("p")
        if paragraphs:
            for paragraph in paragraphs:
                if paragraph.get_text()[:4] != "Save":
                    recipe_text = recipe_text + paragraph.get_text()
    return recipe_name, recipe_text


recipe_links = get_recipes_links(main_page_response)
# Preparing dataframe to save data
recipe_dataframe = pd.DataFrame(columns=["recipe_name", "recipe_text"])
# Iterating over links to get recipe text
for recipe_link in tqdm(recipe_links):
    single_recipe = get_recipe(recipe_link)
    single_recipe_frame = pd.DataFrame({"recipe_name":single_recipe[0],
                                        "recipe_text":single_recipe[1]}, index = [0])
    recipe_dataframe = pd.concat([recipe_dataframe, single_recipe_frame], ignore_index = True)
# Save dataframe as csv file
recipe_dataframe.to_csv("Recipes.csv", index = False)

