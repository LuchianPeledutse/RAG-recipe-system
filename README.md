# Introduction
This pet-project realises a system that helps cook food with certain ingredients. The system is based on RAG paradigm. A lits of recipes is stored in vector database that further facilitates augmented generation with LLM GigaChat. The generation, in turn, provides reciper with additional steps to cook the food.

## Web-crawler
Web crawler collects recipe links from this [website](https://www.simplyrecipes.com/recipes-5090746) and stores them in pandas dataframe along with their names. To run crawler on your machine type the following command:
```bash
python crawler.py
```

