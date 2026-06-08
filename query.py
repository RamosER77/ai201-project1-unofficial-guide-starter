import json
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Load embeddings
with open("embeddings.json", "r") as f:
    data = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")
client = Groq()

def search(query, top_k=3):
    query_embedding = model.encode(query)
    scores = []
    for item in data:
        emb = np.array(item["embedding"])
        score = np.dot(query_embedding, emb) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(emb)
        )
        scores.append((score, item))
    scores.sort(reverse=True, key=lambda x: x[0])
    return [item for _, item in scores[:top_k]]

def ask(question):
    chunks = search(question)
    context = "\n\n".join([
        f"[Source: {c['source']}]\n{c['text']}" for c in chunks
    ])
    prompt = f"""You are a helpful guide for CSUSM students about campus dining.
Answer the question using ONLY the context below. Always cite which source your answer comes from.
If the context doesn't contain the answer, say "I don't have that information."

Context:
{context}

Question: {question}
Answer:"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content, chunks

if __name__ == "__main__":
    print("CSUSM Dining Guide - Ask me anything!")
    print("Type 'quit' to exit\n")
    while True:
        question = input("Your question: ")
        if question.lower() == "quit":
            break
        answer, chunks = ask(question)
        print(f"\nAnswer: {answer}")
        print(f"\nSources used:")
        for c in chunks:
            print(f"  - {c['source']}")
        print()