# Introduction
This pet-project realises a system that helps cook food with certain ingredients. The system is based on RAG paradigm. A lits of recipes is stored in vector database that further facilitates augmented generation with LLM GigaChat. The generation, in turn, provides reciper with additional steps to cook the food.

## Web-crawler
Web crawler collects recipe links from this [website](https://www.simplyrecipes.com/recipes-5090746) parses them and stores parsed text in pandas dataframe along with the names of recipes. To run crawler on your machine type the following command:
```bash
python crawler.py
```
This should create a csv file named 'Recipes.csv' that stores the recipes along with their names.

## System components
The first system component is model called GigaC`hat. To gain access to model visit this [website](https://developers.sber.ru/studio/workspaces/019c8721-a440-702c-bda6-a56bed598931/gigachat-api/projects/019c8721-d6a1-70f0-b538-16aeb1192ffc/parameters) and retrieve access token. This token is needed to run LLMModel class from script systemComponents.
