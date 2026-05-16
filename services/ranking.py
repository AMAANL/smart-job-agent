import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from services.embeddings import get_embedding

job_cache = []

def prepare_jobs(jobs):

    global job_cache

    for job in jobs:

        combined_text = f"""
        Title: {job['title']}
        Domain: {job['domain']}
        Skills: {' '.join(job['skills'])}
        Description: {job['description']}
        """

        embedding = get_embedding(combined_text)

        job_cache.append({
            "job": job,
            "embedding": embedding
        })

def rank_jobs(resume_text):

    enhanced_resume = f"""
    Resume Content:
    {resume_text}

    Extract important:
    - technical skills
    - AI/ML knowledge
    - backend development
    - domains
    - frameworks
    - experience
    """

    resume_embedding = np.array(
        get_embedding(enhanced_resume)
    ).reshape(1, -1)

    ranked_jobs = []

    for item in job_cache:

        job_embedding = np.array(
            item["embedding"]
        ).reshape(1, -1)

        similarity = cosine_similarity(
            resume_embedding,
            job_embedding
        )[0][0]

        skill_overlap = len(
            set(
                resume_text.lower().split()
            ).intersection(
                set(
                    " ".join(
                        item["job"]["skills"]
                    ).lower().split()
                )
            )
        )

        boosted_score = (
            similarity + (skill_overlap * 0.02)
        )

        ranked_jobs.append({
            "id": item["job"]["id"],
            "title": item["job"]["title"],
            "company": item["job"]["company"],
            "location": item["job"]["location"],
            "similarity_score": round(
                float(boosted_score),
                4
            ),
            "job_data": item["job"]
        })

    ranked_jobs.sort(
        key=lambda x: x["similarity_score"],
        reverse=True
    )

    return ranked_jobs[:5]