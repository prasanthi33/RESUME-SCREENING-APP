# app.py
import streamlit as st
import traceback

try:
    from ranker import rank_resumes
except Exception as e:
    st.error("❌ Failed to import `rank_resumes` from `ranker.py`")
    st.text(traceback.format_exc())
    st.stop()

st.set_page_config(page_title="AI Resume Screening System")

st.title("🧠 AI‑Powered Resume Screening System")

st.markdown(
    "📥 Upload one or more resumes and paste the job description below. "
    "The app will return a ranked list based on semantic similarity."
)

uploaded_files = st.file_uploader(
    "📄 Upload Resumes (PDF, DOCX or TXT)",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
)

job_description = st.text_area("📝 Paste Job Description Here", height=200)

if st.button("🔍 Rank Resumes"):
    if not uploaded_files:
        st.warning("⚠️ Please upload at least one resume.")
    elif not job_description.strip():
        st.warning("⚠️ Please provide a job description.")
    else:
        with st.spinner("🔄 Scoring resumes…"):
            try:
                ranked = rank_resumes(uploaded_files, job_description)
                if not ranked:
                    st.info("ℹ️ No matches found.")
                else:
                    st.success("✅ Done!")
                    st.subheader("🏆 Results (Highest Match First)")
                    for name, score in ranked:
                        st.write(f"**{name}** — {score * 100:.2f}% match")
            except Exception as e:
                st.error("❌ Error while ranking resumes.")
                st.text(traceback.format_exc())
