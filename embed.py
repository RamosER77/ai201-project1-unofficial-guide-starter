import os
import json
import numpy as np
from chunk import load_documents, chunk_documents
from sentence_transformers import SentenceTransformer

# Load and chunk documents
print("Loading documents...")
docs = load_documents()
chunks = chunk_documents(docs)
print(f"Total chunks: {len(chunks)}")

# Load embedding model
print("\nLoading embedding model (first time downloads ~90MB)...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Embed all chunks
print("Embedding chunks...")
texts = [chunk["text"] for chunk in chunks]
embeddings = model.encode(texts, show_progress_bar=True)

# Save embeddings + metadata together
print("Saving...")
data = []
for i, chunk in enumerate(chunks):
    data.append({
        "text": chunk["text"],
        "source": chunk["source"],
        "chunk_index": chunk["chunk_index"],
        "embedding": embeddings[i].tolist()
    })

with open("embeddings.json", "w") as f:
    json.dump(data, f)

print(f"\n✅ Done! {len(chunks)} chunks saved to embeddings.json")