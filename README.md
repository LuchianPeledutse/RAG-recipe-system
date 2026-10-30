# Introduction
This pet-project realises a system that helps cook food with certain ingredients. The system is based on RAG paradigm. A lits of recipes is stored in vector database that further facilitates augmented generation with LLM GigaChat. The generation, in turn, provides reciper with additional steps to cook the food.

## Web-crawler
Web crawler collects recipe links from this [website](https://www.simplyrecipes.com/recipes-5090746) parses them and stores parsed text in pandas dataframe along with the names of recipes. To run crawler on your machine type the following command:
```bash
python crawler.py
```
This should create a csv file named 'Recipes.csv' that stores the recipes along with their names.

## System components
The first system component is model called GigaC`hat. To gain access to model visit this [website](https://developers.sber.ru/studio/workspaces/019c8721-a440-702c-bda6-a56bed598931/gigachat-api/projects/019c8721-d6a1-70f0-b538-16aeb1192ffc/parameters) and retrieve access token. This token is needed to run LLMModel class from script systemComponents. The second system component is Knowledge base that is created with faiss and postgreSQL (see below).

## Creating knowledge base
Here we are going to use postgres database along with faiss index to make a knowledge database. The main embedding model that embeds documents along wih queries can be found [here](https://huggingface.co/Snowflake/snowflake-arctic-embed-l-v2.0). To make the code competible on your machine you need to change db link to the link of your chunks database. Then to fill the database with chunks from recipes run fill_knowledge_base.py script.
```bash
python fill_knowledge_base.py
```

## Creating user interface
User interface is realised in command prompt. User provides a single main ingredient (e.g. beef, chicken), the system find 5 chunks that are the closest to main ingredient and adds this data to main dish prompt. Dish prompt asks a model to give recipe backed up by recipe chunks from knowledge base. And the model answer is returned in command prompt. To run command prompt interface run run.py
```bash
python run.py
```

