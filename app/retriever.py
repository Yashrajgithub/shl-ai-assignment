import json
import chromadb

from sentence_transformers import SentenceTransformer
from app.utils import detect_query_type

# -----------------------------
# CONFIG
# -----------------------------

MODEL_NAME = "all-MiniLM-L6-v2"
CHROMA_PATH = "chroma_db"
CATALOG_PATH = "data/catalog.json"

# -----------------------------
# LOAD MODEL
# -----------------------------

print("Loading embedding model...")

model = SentenceTransformer(MODEL_NAME)

print("Model loaded.")

# -----------------------------
# LOAD CHROMADB
# -----------------------------

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_collection(
    name="shl_assessments"
)

print("ChromaDB loaded.")

# -----------------------------
# LOAD RAW CATALOG
# -----------------------------

with open(CATALOG_PATH, "r", encoding="utf-8") as f:

    raw_json = f.read()

    raw_json = raw_json.replace("\n", " ")
    raw_json = raw_json.replace("\r", " ")
    raw_json = raw_json.replace("\t", " ")

    catalog = json.loads(raw_json, strict=False)

print(f"Loaded {len(catalog)} catalog items.")

# -----------------------------
# KEYWORD BOOST FUNCTION
# -----------------------------

def keyword_score(query, text):

    score = 0

    query_words = query.lower().split()

    text = text.lower()

    for word in query_words:

        if word in text:
            score += 1

    return score

# -----------------------------
# SEARCH FUNCTION
# -----------------------------

def search_assessments(query, top_k=5):

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=25
    )

    metadata = results["metadatas"][0]
    documents = results["documents"][0]

    detected = detect_query_type(query)

    scored_results = []

    for meta, doc in zip(metadata, documents):

        keyword_boost = keyword_score(query, doc)

        category_boost = 0

        categories = meta.get("keys", "").lower()
        name = meta.get("name", "").lower()

        # TECHNICAL BOOST

        if detected["technical"]:

            tech_keywords = [
                "java",
                "python",
                "sql",
                "react",
                "node",
                "backend",
                "frontend",
                "developer",
                "programming",
                "coding",
                "software"
            ]

            for word in tech_keywords:
                name_words = name.split()
                doc_words = doc.lower().split()

                if word in name_words:
                    category_boost += 5

                if word in doc_words:
                    category_boost += 2

            if "knowledge & skills" in categories:
                category_boost += 3

            if "simulation" in categories:
                category_boost += 2

        # COMMUNICATION BOOST

        if detected["communication"]:

            if "interpersonal communications" in name:
                category_boost += 8

            if "business communication" in name:
                category_boost += 8

            if "communication" in name:
                category_boost += 3

            if "interpersonal" in name:
                category_boost += 3

            if "personality" in categories:
                category_boost += 1

            if "competencies" in categories:
                category_boost += 1

        # PERSONALITY BOOST

        if detected["personality"]:

            if "personality" in categories:
                category_boost += 5

            if "opq" in name:
                category_boost += 5

        final_score = keyword_boost + category_boost

        scored_results.append({
            "score": final_score,
            "meta": meta
        })

    # Remove duplicates

    unique_results = {}

    for item in scored_results:

        name = item["meta"]["name"]

        if name not in unique_results:
            unique_results[name] = item

    scored_results = list(unique_results.values())

    # Sort descending

    scored_results = sorted(
        scored_results,
        key=lambda x: x["score"],
        reverse=True
    )

    return scored_results[:top_k]

# -----------------------------
# TEST SEARCH
# -----------------------------

if __name__ == "__main__":

    query = "Hiring Java backend developer with communication skills"

    print(f"\nQuery: {query}\n")

    results = search_assessments(query)

    for idx, item in enumerate(results, start=1):

        meta = item["meta"]

        print("=" * 60)

        print(f"Result #{idx}")

        print(f"Name: {meta['name']}")

        print(f"Categories: {meta['keys']}")

        print(f"URL: {meta['url']}")

        print(f"Score: {item['score']}")

        print(f"Description: {meta['description'][:200]}")

        print()