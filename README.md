# Smart Job Match Agent

AI-powered job recommendation system built using FastAPI, semantic embeddings, cosine similarity, and Groq LLM tool-calling.

## Features

- Semantic job matching using sentence embeddings
- Cosine similarity ranking
- Real LLM tool-calling for resume parsing
- AI-generated match explanations
- Dynamic clarifying question generation
- Bonus `/refine` endpoint for reranking
- FastAPI REST API
- Vercel deployment ready

---

# Tech Stack

- FastAPI
- Groq API
- Hugging Face Inference API (BAAI/bge-small-en-v1.5 embeddings)
- scikit-learn
- NumPy
- Python

---

# Project Structure

```bash
job_ai/
│
├── api/
│   └── index.py
│
├── services/
│   ├── embeddings.py
│   ├── ranking.py
│   ├── llm_agent.py
│   └── prompts.py
│
├── data/
│   └── jobs.json
│
├── requirements.txt
├── vercel.json
├── README.md
├── WRITEUP.md
└── .env.example
```

---

# Setup Instructions

## 1. Clone Repository

```bash
git clone <your_repo_url>
cd job_ai
```

## 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## 4. Add Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_api_key_here
```

---

# Run Locally

```bash
python3 -m uvicorn api.index:app --reload
```

Open:

```bash
http://127.0.0.1:8000/docs
```

---

# API Endpoints

## POST `/recommend`

Request:

```json
{
  "resume_text": "Python developer with NLP and FastAPI experience"
}
```

Returns:
- Parsed candidate profile
- Top matched jobs
- Match explanations
- Clarifying question

---

## POST `/refine`

Request:

```json
{
  "resume_text": "resume text",
  "clarifying_question": "question",
  "candidate_answer": "I prefer NLP roles"
}
```

Returns:
- Updated ranked jobs
- Refinement reasoning

---

# Deployment

The project is configured for deployment on Vercel using:

```json
vercel.json
```

---

# Design Highlights

- Job embeddings are generated and cached at startup using the Hugging Face hosted embedding API.
- Semantic ranking is performed using embedding similarity and cosine similarity scoring.
- Groq tool-calling is used for structured resume extraction
- Resume/job matching is separated from reasoning for modularity

---

# Future Improvements

- Add vector database support
- Add authentication and rate limiting
- Improve reranking using structured candidate preferences
- Async explanation generation
- Conversation memory for multi-turn refinement
