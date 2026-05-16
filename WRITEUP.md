# WRITEUP.md

# 1. Design Choices

I used the `sentence-transformers/all-MiniLM-L6-v2` embedding model for semantic similarity ranking. This model was selected because it is lightweight, fast, and suitable for deployment within Vercel’s memory and execution constraints. The model provides good semantic retrieval quality while keeping inference latency low.

I considered larger embedding models such as BGE-large and MPNet, but rejected them because they would significantly increase cold start time and memory usage during deployment. Since the assignment dataset contains only 50 jobs, a lightweight embedding model was sufficient.

For ranking, I used cosine similarity between the resume embedding and precomputed job embeddings. In addition to semantic similarity, I implemented lightweight lexical skill-overlap boosting to improve precision for technical skill matching.

I used Groq’s `llama-3.3-70b-versatile` model for reasoning and tool-calling because it offers fast inference and supports structured tool usage while remaining free and easy to deploy.

---

# 2. Agentic Architecture

The system uses a two-step agentic workflow:

1. Resume Parsing Tool
2. Match Reasoning Layer

The first tool extracts structured information from raw resume text using Groq function/tool calling. The parser returns:
- candidate name
- skills
- experience
- preferred roles
- education

The second reasoning layer takes the top-ranked jobs from semantic retrieval and generates recruiter-style explanations for why each role is or is not a good fit.

I intentionally separated retrieval from reasoning:
- semantic embeddings handle scalable ranking
- the LLM handles interpretation and explanation

This separation improves modularity, debuggability, and reliability compared to a single large prompt chain.

Potential failure modes:
- incorrect resume parsing
- hallucinated missing skills
- weak rankings for extremely short resumes
- semantic confusion when resumes contain unrelated technologies

---

# 3. Honest Weaknesses

The system may struggle with:
- noisy resumes
- resumes with poor formatting
- resumes containing excessive non-technical content
- ambiguous role preferences

Because embeddings are generated from raw text, poorly written resumes can reduce semantic retrieval quality.

At scale (10,000+ concurrent requests), the current architecture would face:
- inference bottlenecks
- increased cold starts
- memory pressure
- API rate limiting

The current implementation also performs explanation generation sequentially, which increases latency.

Due to time constraints, I intentionally avoided:
- vector databases
- async batching
- distributed caching
- authentication
- advanced reranking pipelines
- conversation memory

The `/refine` endpoint currently performs lightweight reranking by augmenting the resume context rather than maintaining long-term structured conversational state.

---

# 4. Next Steps

If I had two more days, the highest-impact improvement would be implementing a dedicated reranking stage using cross-encoder models.

Currently, the system relies primarily on embedding similarity. A cross-encoder reranker would improve precision by jointly evaluating resume-job pairs rather than comparing embeddings independently.

This would significantly improve:
- ranking accuracy
- domain understanding
- handling of nuanced technical matches

I would also add:
- async explanation generation
- vector database support
- stronger candidate preference modeling
- conversation memory for multi-turn refinement
- better prompt evaluation and monitoring