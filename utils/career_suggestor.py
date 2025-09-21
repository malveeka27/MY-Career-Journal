import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel

# ---------------- Vertex AI Initialization ----------------
PROJECT_ID = "textdemo-472317"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

# LOADING GEMINI 2.0 MODEL
model = GenerativeModel("gemini-2.0-flash")

#FUCTION SUGGEST A CAREER BASED ON INPUT
def suggest_career_ai(skills: str, aptitude_score: int):
    """
    Suggest careers based on skills and aptitude score using Vertex AI.

    Parameters:
        skills (str): Comma-separated skills
        aptitude_score (int): User's aptitude test score

    Returns:
        list: Suggested career roles
    """
    skills_list = [s.strip() for s in skills.split(",") if s.strip()]
    if not skills_list:
        return ["Please enter at least one skill"]

    prompt = f"""
    Based on the following inputs:
    - Skills: {', '.join(skills_list)}
    - Aptitude Score: {aptitude_score}

    Suggest 5 suitable career options.
    Provide only the career titles in a simple numbered list.
    """

    try:
        response = model.generate_content(prompt)
        text = response.candidates[0].content.parts[0].text.strip()
        careers = [line.strip(" -1234567890.") for line in text.split("\n") if line.strip()]
        return careers
    except Exception as e:
        st.error(f"Error generating career suggestions: {e}")
        return []



