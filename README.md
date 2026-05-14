# SHL Conversational Assessment Recommender

AI-powered conversational recommendation agent for SHL assessments.

## Features

- Conversational SHL assessment recommendation
- Semantic retrieval using ChromaDB
- Hybrid ranking with keyword boosting
- Multi-turn conversational refinement
- Grounded responses using SHL catalog
- Comparison support (e.g. OPQ vs GSA)
- Refusal handling for off-topic queries
- FastAPI backend
- Swagger API docs

---

## Tech Stack

- FastAPI
- Python
- ChromaDB
- Sentence Transformers
- Gemini 2.5 Flash

---

## Setup

### Clone repository

```bash
git clone <repo-url>
cd shl-ai-assignment
```

### Create virtual environment

```bash
python -m venv venv
```

### Activate virtual environment

Windows:

```bash
venv\Scripts\activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
uvicorn main:app --reload
```

---

## API Docs

```text
http://127.0.0.1:8000/docs
```

---

## Endpoints

### Health Check

```http
GET /health
```

### Conversational Chat

```http
POST /chat
```

---

## Deployment

Deployable on:
- Render
- Railway
- HuggingFace Spaces

---

## Author

Yashraj Kalshetti