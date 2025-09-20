"""Compute semantic similarity between resumes and a job description."""

from sentence_transformers import SentenceTransformer, util
from resume_parser import extract_text

# Load the Sentence‑BERT model once at import time
_model = SentenceTransformer("all-MiniLM-L6-v2")


def rank_resumes(uploaded_files, job_description: str):
    """Return a list of tuples (filename, similarity_score) sorted high→low."""
    jd_emb = _model.encode(job_description, convert_to_tensor=True)
    results = []

    for file in uploaded_files:
        try:
            text = extract_text(file)
        except Exception as e:
            # Skip unreadable files but keep the app running
            results.append((file.name + " (error)", 0))
            continue

        res_emb = _model.encode(text, convert_to_tensor=True)
        score = util.pytorch_cos_sim(jd_emb, res_emb).item()
        results.append((file.name, score))

    # Highest similarity first
    return sorted(results, key=lambda x: x[1], reverse=True)