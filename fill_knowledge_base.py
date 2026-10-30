import pandas as pd
from tqdm import tqdm

from systemComponents import KnowledgeBase

recipe_data = pd.read_csv("Recipes.csv")
recipe_texts = recipe_data['recipe_text']

base = KnowledgeBase()

for recipe_text in tqdm(recipe_texts, desc = "Adding recipes to knowledge base..."):
    batched_chunks = []
    for batch_idx in range(len(recipe_text)//300):
        current_batch = recipe_text[batch_idx*300:(batch_idx+1)*300 if (batch_idx + 1)*300 < len(recipe_text) else len(recipe_text)]
        batched_chunks.append(current_batch)
    base.add_chunks(batched_chunks)

base.save_index("vector_index.index")

