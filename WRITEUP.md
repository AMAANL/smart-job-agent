
---

# WRITEUP.md

```md id="jlwmpL"
# WRITEUP

# 1. Design Choices

I initially selected the `sentence-transformers/all-MiniLM-L6-v2` model because it is lightweight, widely used for semantic similarity tasks, and performs well for embedding-based retrieval systems. The goal of the system was to generate embeddings for resumes and job descriptions and compute cosine similarity between them for semantic ranking.

However, while deploying to Vercel, I encountered serverless deployment limitations. The local sentence-transformers pipeline required PyTorch and transformer dependencies, which exceeded Vercel’s Lambda bundle size and memory constraints on the free tier.

To solve this, I migrated embedding generation to the Hugging Face hosted inference API while preserving the same semantic retrieval architecture. This significantly reduced deployment size and improved compatibility with serverless infrastructure.

Alternative approaches considered:
- OpenAI embeddings
- Cohere embeddings
- Local sentence-transformers pipeline

I rejected OpenAI and Cohere mainly to avoid paid API usage and additional account setup complexity. I also rejected keeping the local transformer pipeline because it was not practical within Vercel free-tier constraints.

Trade-offs:
- Hosted embeddings reduce deployment complexity
- Slightly higher network latency due to API calls
- Better production compatibility and scalability

---

# 2. Agentic Architecture

The system follows a multi-step agentic pipeline:

1. Resume Parsing Agent
   - Uses Groq tool-calling to extract structured candidate data from raw resume text.
   - Extracted fields include skills, preferred roles, education, and experience.

2. Embedding + Ranking Tool
   - Resume and job descriptions are converted into embeddings.
   - Cosine similarity is computed between vectors to rank jobs semantically.

3. Explanation Generation Agent
   - The LLM generates detailed explanations describing why each job matches the candidate profile.

4. Clarification Question Agent
   - The system generates a follow-up question when candidate preferences or experience are ambiguous.

5. Refine Endpoint
   - Candidate clarification responses are merged back into the profile.
   - Rankings are recomputed dynamically.

I intentionally separated the workflow into multiple tool-style stages instead of one large prompt because:
- it improves modularity,
- allows independent debugging,
- makes ranking deterministic,
- and reduces hallucination risk.

Failure modes:
- Weak resumes with limited technical keywords may reduce embedding quality.
- Ambiguous resumes can produce incomplete structured extraction.
- LLM-generated explanations may occasionally overestimate candidate suitability.

---

# 3. Honest Weaknesses

The system still has several limitations.

Poorly written resumes with minimal technical detail may produce weak semantic embeddings and inaccurate rankings. Since embedding quality depends heavily on textual clarity, vague resumes can reduce recommendation quality.

The system is also not optimized for high-scale production traffic. At 10,000 concurrent requests:
- repeated embedding API calls could become slow,
- serverless cold starts may increase latency,
- and external API rate limits could become bottlenecks.

Several engineering shortcuts were taken due to time constraints:
- no caching layer for embeddings,
- no database persistence,
- no async batching,
- and no advanced reranking architecture.

The recommendation engine currently relies purely on embedding similarity and does not incorporate:
- weighting by experience,
- seniority alignment,
- or company/domain preferences.

Pure embedding similarity can sometimes over-generalize toward semantically related technical domains. A future improvement would combine semantic retrieval with explicit skill-weighting and rule-based constraints.

---

# 4. Next Steps

If I had two more days, the highest-impact improvement would be implementing a hybrid retrieval and reranking pipeline.

Currently, ranking depends only on embedding similarity. I would improve this by adding:
- embedding retrieval for recall,
- followed by LLM reranking for precision.

This would significantly improve recommendation quality because:
- embeddings are good at semantic retrieval,
- while LLM reranking is better at nuanced reasoning.

I would also add:
- embedding caching,
- async processing,
- vector database support,
- and stronger resume normalization.

These improvements would make the system more production-ready and scalable while improving ranking accuracy.
