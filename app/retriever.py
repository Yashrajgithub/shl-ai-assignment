import json

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.metrics.pairwise import cosine_similarity

from app.utils import detect_query_type


# -----------------------------
# LOAD CATALOG
# -----------------------------

CATALOG_PATH = "data/catalog.json"


with open(CATALOG_PATH, "r", encoding="utf-8") as f:

    raw_json = f.read()

    raw_json = raw_json.replace("\n", " ")

    raw_json = raw_json.replace("\r", " ")

    raw_json = raw_json.replace("\t", " ")

    catalog = json.loads(raw_json, strict=False)


print(f"Loaded {len(catalog)} catalog items.")


# -----------------------------
# PREPARE SEARCH TEXTS
# -----------------------------

documents = []

for item in catalog:

    text = f"""
    {item.get('name', '')}
    {item.get('description', '')}
    {' '.join(item.get('keys', []))}
    {' '.join(item.get('job_levels', []))}
    """

    documents.append(text)


# -----------------------------
# TF-IDF
# -----------------------------

vectorizer = TfidfVectorizer(
    stop_words="english"
)

tfidf_matrix = vectorizer.fit_transform(documents)


# -----------------------------
# KEYWORD SCORE
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
# SEARCH
# -----------------------------

def search_assessments(query, top_k=4):

    query_vector = vectorizer.transform([query])

    similarities = cosine_similarity(
        query_vector,
        tfidf_matrix
    ).flatten()

    detected = detect_query_type(query)

    scored_results = []

    for idx, sim_score in enumerate(similarities):

        item = catalog[idx]

        name = item.get("name", "").lower()

        description = item.get("description", "").lower()

        categories = " ".join(
            item.get("keys", [])
        ).lower()

        text = f"{name} {description}"

        keyword_boost = keyword_score(query, text)

        category_boost = 0


        # TECHNICAL

        if detected["technical"]:

            if "java" in query.lower():

                if "java" in name.split():
                    category_boost += 5

            if "knowledge & skills" in categories:
                category_boost += 2


        # COMMUNICATION

        if detected["communication"]:

            if "communication" in name:
                category_boost += 5

            if "interpersonal" in name:
                category_boost += 5


        # PERSONALITY

        if detected["personality"]:

            if "personality" in categories:
                category_boost += 5

            if "opq" in name:
                category_boost += 5


        final_score = (
            sim_score * 10
            + keyword_boost
            + category_boost
        )

        scored_results.append({
            "score": final_score,
            "meta": {
                "name": item.get("name", ""),
                "url": item.get("link", ""),
                "description": item.get("description", ""),
                "keys": ", ".join(item.get("keys", []))
            }
        })


    scored_results = sorted(
        scored_results,
        key=lambda x: x["score"],
        reverse=True
    )

    return scored_results[:top_k]