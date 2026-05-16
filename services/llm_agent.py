from groq import Groq
from dotenv import load_dotenv
import os
import json

from services.prompts import (
    MATCH_EXPLANATION_PROMPT,
    QUESTION_PROMPT
)

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "llama-3.3-70b-versatile"

def parse_resume(resume_text):

    tools = [
        {
            "type": "function",
            "function": {
                "name": "extract_resume",
                "description": "Extract candidate details",
                "parameters": {
                    "type": "object",
                    "properties": {

    "name": {
        "type": ["string", "null"]
    },

    "skills": {
        "type": "array",
        "items": {
            "type": "string"
        }
    },

    "experience_years": {
    "type": ["number", "string", "null"]
},

    "preferred_roles": {
    "type": ["array", "string", "null"],
        "items": {
            "type": "string"
        }
    },

    "education": {
        "type": ["string", "null"]
    }
},
                    "required": ["skills"]
                }
            }
        }
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
    {
        "role": "system",
        "content": """
        You are a resume parser.

        Extract structured candidate data.

        Rules:
        - Do not hallucinate
        - If field missing return null
        - Skills must be technical
        """
    },
    {
        "role": "user",
        "content": resume_text
    }
],
        tools=tools,
        tool_choice="auto"
    )

    tool_call = response.choices[0].message.tool_calls[0]

    arguments = json.loads(
        tool_call.function.arguments
    )
    tool_call = response.choices[0].message.tool_calls[0]

    arguments = json.loads(
        tool_call.function.arguments
    )

    if arguments.get("preferred_roles") == "null":
        arguments["preferred_roles"] = []

    if arguments.get("preferred_roles") is None:
        arguments["preferred_roles"] = []

    if arguments.get("experience_years") == "null":
        arguments["experience_years"] = None

    if arguments.get("name") == "null":
        arguments["name"] = None

    if arguments.get("education") == "null":
        arguments["education"] = None

    return arguments
    return arguments

def generate_explanations(candidate, ranked_jobs):

    final_jobs = []

    for job in ranked_jobs:

        prompt = MATCH_EXPLANATION_PROMPT.format(
            candidate=candidate,
            job=job["job_data"]
        )

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        explanation = response.choices[0].message.content

        final_jobs.append({
            "id": job["id"],
            "title": job["title"],
            "company": job["company"],
            "similarity_score": job["similarity_score"],
            "explanation": explanation
        })

    return final_jobs

def generate_question(candidate, jobs):

    prompt = QUESTION_PROMPT.format(
        candidate=candidate,
        jobs=jobs
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content