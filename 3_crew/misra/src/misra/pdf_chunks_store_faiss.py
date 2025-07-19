import openai
import faiss
import numpy as np
import json
import tiktoken
 # your API key

with open("misra_rules.json") as f:
    chunks = json.load(f)

texts = [chunk['rule'] for chunk in chunks]

def get_embedding(text):
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

vectors = [get_embedding(t) for t in texts]
dimension = len(vectors[0])

index = faiss.IndexFlatL2(dimension)
index.add(np.array(vectors))

faiss.write_index(index, "misra_openai.faiss")
with open("misra_texts.json", "w") as f:
    json.dump(texts, f)

print("[✓] Stored MISRA chunks using OpenAI embeddings.")
