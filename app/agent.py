import os
import json

import google.generativeai as genai

from dotenv import load_dotenv

from app.retriever import search_assessments


# -----------------------------
# LOAD ENV
# -----------------------------

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)


# -----------------------------
# LOAD MODEL
# -----------------------------

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


# -----------------------------
# REFUSAL CHECK
# -----------------------------

OUT_OF_SCOPE_KEYWORDS = [
    "salary",
    "legal",
    "law",
    "court",
    "politics",
    "religion",
    "hack",
    "bypass",
    "ignore instructions"
]


def is_out_of_scope(text):

    text = text.lower()

    for word in OUT_OF_SCOPE_KEYWORDS:

        if word in text:
            return True

    return False


# -----------------------------
# BUILD CONVERSATION CONTEXT
# -----------------------------

def build_conversation(messages):

    conversation = ""

    for msg in messages:

        role = msg["role"]

        content = msg["content"]

        conversation += f"{role.upper()}: {content}\n"

    return conversation


# -----------------------------
# DETECT CLARIFICATION NEED
# -----------------------------

def needs_clarification(user_message):

    vague_terms = [
        "assessment",
        "test",
        "hiring",
        "candidate"
    ]

    user_message = user_message.lower()

    word_count = len(user_message.split())

    if word_count <= 3:
        return True

    matched = 0

    for word in vague_terms:

        if word in user_message:
            matched += 1

    if matched >= 1 and word_count < 6:
        return True

    return False


# -----------------------------
# MAIN AGENT FUNCTION
# -----------------------------

def generate_response(messages):

    latest_user_message = messages[-1]["content"]

    conversation_context = build_conversation(messages)

    user_messages = []
    for msg in messages:
        if msg["role"] == "user":
            user_messages.append(msg["content"])

    enhanced_query = " ".join(user_messages)

    normalized_message = latest_user_message.lower()

    if "gsa" in normalized_message:
        latest_user_message += " Global Skills Assessment"

    # -----------------------------
    # OUT OF SCOPE
    # -----------------------------

    if is_out_of_scope(latest_user_message):

        return {
            "reply": (
                "I can only help with SHL assessment recommendations "
                "and comparisons from the SHL catalog."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # CLARIFICATION
    # -----------------------------

    if needs_clarification(latest_user_message):

        return {
            "reply": (
                "Could you share more details about the role, "
                "skills, seniority level, or assessment needs?"
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # RETRIEVAL
    # -----------------------------

    retrieved = search_assessments(
        enhanced_query,
        top_k=4
    )

    # -----------------------------
    # BUILD GROUNDING CONTEXT
    # -----------------------------

    retrieval_context = ""

    recommendations = []

    for item in retrieved:

        meta = item["meta"]

        retrieval_context += f"""
        Assessment Name: {meta['name']}
        Description: {meta['description']}
        Categories: {meta['keys']}
        URL: {meta['url']}
        """

        recommendations.append({
            "name": meta["name"],
            "url": meta["url"],
            "test_type": meta["keys"]
        })

    # -----------------------------
    # CONVERSATION
    # -----------------------------

    conversation = build_conversation(messages)

    # -----------------------------
    # PROMPT
    # -----------------------------

    prompt = f"""
    You are an SHL assessment recommendation assistant.

    STRICT RULES:
    - ONLY recommend assessments from provided context.
    - NEVER hallucinate assessment names.
    - NEVER recommend anything outside SHL catalog.
    - Keep answers concise and professional.
    - Support hiring recommendations.
    - Support comparison questions.
    - Use ONLY grounded catalog data.

    Conversation:
    {conversation}

    Retrieved SHL Assessments:
    {retrieval_context}

    Generate a concise assistant reply.
    """

    # -----------------------------
    # LLM GENERATION
    # -----------------------------

    response = model.generate_content(prompt)

    reply = response.text.strip()

    # -----------------------------
    # END CONVERSATION DETECTION
    # -----------------------------

    end_conversation = False

    closing_terms = [
        "thanks",
        "thank you",
        "done",
        "great",
        "perfect"
    ]

    for term in closing_terms:

        if term in latest_user_message.lower():
            end_conversation = True
            break

    return {
        "reply": reply,
        "recommendations": recommendations,
        "end_of_conversation": end_conversation
    }