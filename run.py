import faiss
import warnings
warnings.filterwarnings("ignore")


from systemComponents import LLMModel, KnowledgeBase


# Load filled index and main database
main_index = faiss.read_index("vector_index.index")
main_db = KnowledgeBase(faiss_index = main_index)
# Prepaing models and prompts
llm_model = LLMModel()

def dish_prompt(dish, context):
    text = f"Suggest a recipe for the {dish} dish. Take into account the following context:\n{context}"
    return text

# Main app
while True:
    user_input = input("Select dish item...")
    retrieved_chunks = main_db.retrieve(user_input)
    chunk_context = "".join(retrieved_chunks)
    response = llm_model.generate(dish_prompt(user_input, chunk_context))
    print(response, end = '\n\n')
    
    