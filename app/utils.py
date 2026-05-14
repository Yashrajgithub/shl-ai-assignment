TECH_KEYWORDS = [
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
    "software",
    "engineering",
    "aws",
    "cloud",
    "data science",
    "machine learning"
]


COMMUNICATION_KEYWORDS = [
    "communication",
    "stakeholder",
    "client",
    "presentation",
    "collaboration",
    "teamwork",
    "leadership"
]


PERSONALITY_KEYWORDS = [
    "personality",
    "behavior",
    "cultural fit",
    "motivation",
    "soft skills"
]


def detect_query_type(query):

    query = query.lower()

    detected = {
        "technical": False,
        "communication": False,
        "personality": False
    }

    for word in TECH_KEYWORDS:

        if word in query:
            detected["technical"] = True

    for word in COMMUNICATION_KEYWORDS:

        if word in query:
            detected["communication"] = True

    for word in PERSONALITY_KEYWORDS:

        if word in query:
            detected["personality"] = True

    return detected