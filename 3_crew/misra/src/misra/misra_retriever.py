import openai
import faiss
import numpy as np
import json

# Load vector DB and texts
index = faiss.read_index("misra_openai.faiss")
with open("misra_texts.json", "r", encoding="utf-8") as f:
    misra_texts = json.load(f)

def get_query_embedding(text):
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding, dtype="float32")

def retrieve_misra_rules(query: str, k=5) -> str:
    query_vec = np.array([get_query_embedding(query)])
    distances, indices = index.search(query_vec, k)
    return "\n\n".join([misra_texts[i] for i in indices[0]])
