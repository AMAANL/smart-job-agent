from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import json

from services.ranking import (
    prepare_jobs,
    rank_jobs
)

from services.llm_agent import (
    parse_resume,
    generate_explanations,
    generate_question
)

app = FastAPI(
    title="Smart Job Match Agent"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("data/jobs.json", "r") as f:
    jobs = json.load(f)

prepare_jobs(jobs)

class ResumeRequest(BaseModel):
    resume_text: str
class RefineRequest(BaseModel):
    resume_text: str
    clarifying_question: str
    candidate_answer: str

@app.get("/")
def home():

    return {
        "message": "API running"
    }

@app.post("/recommend")
def recommend(req: ResumeRequest):

    if len(req.resume_text.strip()) < 20:

        raise HTTPException(
            status_code=400,
            detail="Resume text too short"
        )

    candidate = parse_resume(
        req.resume_text
    )
    structured_resume = f"""
Candidate Name:
{candidate.get('name')}

Technical Skills:
{', '.join(candidate.get('skills') or [])}
Preferred Roles:
{', '.join(candidate.get('preferred_roles') or [])}
Education:
{candidate.get('education')}

Original Resume:
{req.resume_text}
"""

    ranked_jobs = rank_jobs(
        structured_resume
        )

    explained_jobs = generate_explanations(
        candidate,
        ranked_jobs
    )

    question = generate_question(
        candidate,
        explained_jobs
    )

    return {
        "candidate": {
            "name": candidate.get("name"),
            "skills": candidate.get("skills"),
            "experience_years":
                candidate.get("experience_years")
        },
        "ranked_jobs": explained_jobs,
        "clarifying_question": question
    }

@app.post("/refine")
def refine(req: RefineRequest):

    updated_resume = f"""
    Original Resume:
    {req.resume_text}

    Candidate Clarification:
    {req.candidate_answer}
    """

    candidate = parse_resume(
        updated_resume
    )

    structured_resume = f"""
Candidate Name:
{candidate.get('name')}

Technical Skills:
{', '.join(candidate.get('skills') or [])}

Preferred Roles:
{', '.join(candidate.get('preferred_roles') or [])}

Education:
{candidate.get('education')}

Resume:
{updated_resume}
"""

    reranked = rank_jobs(
        structured_resume
    )

    explained_jobs = generate_explanations(
        candidate,
        reranked
    )

    return {
        "ranked_jobs": explained_jobs,
        "reasoning":
        "Job rankings were updated using the candidate's clarification response."
    }