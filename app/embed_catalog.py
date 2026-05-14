import json
import chromadb

from sentence_transformers import SentenceTransformer


# -----------------------------
# CONFIG
# -----------------------------

MODEL_NAME = "all-MiniLM-L6-v2"

CATALOG_PATH = "data/catalog.json"

CHROMA_PATH = "chroma_db"


# -----------------------------
# LOAD EMBEDDING MODEL
# -----------------------------

print("Loading embedding model...")

model = SentenceTransformer(MODEL_NAME)

print("Model loaded.")


# -----------------------------
# CREATE CHROMA CLIENT
# -----------------------------

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name="shl_assessments"
)


# -----------------------------
# LOAD CATALOG
# -----------------------------

with open(CATALOG_PATH, "r", encoding="utf-8") as f:

    raw_json = f.read()

    # Remove problematic control characters
    raw_json = raw_json.replace("\n", " ")

    raw_json = raw_json.replace("\r", " ")

    raw_json = raw_json.replace("\t", " ")

    catalog = json.loads(raw_json, strict=False)

print(f"Loaded {len(catalog)} assessments.")


# -----------------------------
# PROCESS EACH ASSESSMENT
# -----------------------------

for idx, item in enumerate(catalog):

    name = item.get("name", "")

    description = item.get("description", "")

    job_levels = ", ".join(item.get("job_levels", []))

    keys = ", ".join(item.get("keys", []))

    duration = item.get("duration", "")

    languages = ", ".join(item.get("languages", []))

    remote = item.get("remote", "")

    adaptive = item.get("adaptive", "")

    url = item.get("link", "")

    # IMPORTANT:
    # This text is what semantic search understands

    search_text = f"""
    Assessment Name: {name}

    Description:
    {description}

    Job Levels:
    {job_levels}

    Categories:
    {keys}

    Duration:
    {duration}

    Languages:
    {languages}

    Remote Testing:
    {remote}

    Adaptive Testing:
    {adaptive}
    """

    # Create embedding

    embedding = model.encode(search_text).tolist()

    # Store in ChromaDB

    collection.add(
        ids=[str(idx)],

        embeddings=[embedding],

        documents=[search_text],

        metadatas=[{
            "name": name,
            "url": url,
            "description": description,
            "keys": keys,
            "job_levels": job_levels,
            "duration": duration
        }]
    )

    print(f"Added: {name}")


print("\nEmbedding pipeline complete.")