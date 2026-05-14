# SHL Conversational Assessment Recommender – Approach Document

## Overview

This project implements a conversational AI agent for recommending SHL assessments based on user hiring requirements.

The system supports:
- Conversational recommendations
- Multi-turn refinement
- Assessment comparisons
- Clarification handling
- Off-topic refusal handling

The solution is built using FastAPI and grounded entirely on the provided SHL assessment catalog.

---

# Architecture

User Query
→ FastAPI API
→ Conversational Agent
→ Retrieval Engine
→ Gemini LLM
→ Structured JSON Response

---

# Retrieval Strategy

The system uses a lightweight hybrid retrieval approach:

- TF-IDF semantic similarity
- Keyword-based boosting
- Intent-aware reranking

This approach was selected because:
- The catalog size is relatively small
- TF-IDF provides fast and memory-efficient retrieval
- Lightweight deployment improves cloud reliability

Additional heuristic reranking improves:
- Technical assessment matching
- Communication/personality assessment discovery
- Conversational refinement handling

---

# Conversational Design

The agent reconstructs conversational context using prior user messages.

Supported flows:
- Clarification requests
- Refinement queries
- Assessment comparisons
- Multi-turn conversations

Example:
- "Need backend developer assessment"
- "Also include personality and communication tests"

The system combines both turns for improved retrieval relevance.

---

# Grounding & Hallucination Prevention

To reduce hallucinations:
- Recommendations are generated only from retrieved SHL catalog entries
- The LLM is explicitly instructed to avoid external recommendations
- Comparison responses are grounded on retrieved catalog descriptions

---

# Guardrails

The system rejects:
- Hacking/prompt injection attempts
- Legal advice
- Non-SHL recommendation requests
- Off-topic conversations

---

# Deployment

The application is deployed on Render using:
- FastAPI
- Python
- Gemini 2.5 Flash

Public API:
https://shl-ai-assignment-cqwt.onrender.com

GitHub Repository:
https://github.com/Yashrajgithub/shl-ai-assignment

---

# Limitations

- Free-tier deployment may introduce cold-start latency
- Retrieval quality depends on catalog metadata quality
- Lightweight retrieval may occasionally miss nuanced semantic relationships

---

# Future Improvements

- Cross-encoder reranking
- Better conversational memory modeling
- Structured comparison templates
- Adaptive recommendation diversification