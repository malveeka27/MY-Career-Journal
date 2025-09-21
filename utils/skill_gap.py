import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel

# SETTING UP VERTEX AI
PROJECT_ID = "textdemo-472317"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

# LOADING GEMINI
model = GenerativeModel("gemini-2.0-flash")

#USES GEMININ AND VERTEX AI TO RETURN A STABLE OF MISSING SKILLS AND STUDY MATERIALS
def analyze_skill_gap(skills: str, target_role: str):

    skills_list = [s.strip() for s in skills.split(",") if s.strip()]
    prompt = f"""
    The user has the following skills: {skills_list}.
    The target job role is: {target_role}.

    Provide the missing skills in a **Markdown table** with 2 columns:
    | Missing Skill | Learning Resources |
    Only return the table, no explanations.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error in skill gap analysis: {e}")
        # FALLBACK TABLE
        return """
        | Missing Skill | Learning Resources |
        |---------------|---------------------|
        | Python        | [Python.org](https://www.python.org/) |
        | SQL           | [W3Schools SQL](https://www.w3schools.com/sql/) |
        | Machine Learning | [Coursera](https://www.coursera.org/) |
        """


