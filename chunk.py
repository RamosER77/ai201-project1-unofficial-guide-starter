import os

def load_documents(folder="documents"):
    docs = []
    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(folder, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
            docs.append({
                "filename": filename,
                "text": text
            })
            print(f"✅ Loaded {filename} ({len(text)} chars)")
    return docs

def chunk_text(text, chunk_size=300, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def chunk_documents(docs):
    all_chunks = []
    for doc in docs:
        chunks = chunk_text(doc["text"])
        for i, chunk in enumerate(chunks):
            all_chunks.append({
                "source": doc["filename"],
                "chunk_index": i,
                "text": chunk
            })
    return all_chunks

if __name__ == "__main__":
    docs = load_documents()
    print(f"\nLoaded {len(docs)} documents")
    
    chunks = chunk_documents(docs)
    print(f"Created {len(chunks)} chunks")
    print(f"\nExample chunk from {chunks[0]['source']}:")
    print(chunks[0]['text'][:200])