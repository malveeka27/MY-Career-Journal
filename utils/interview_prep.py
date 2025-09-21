import vertexai
from vertexai.generative_models import GenerativeModel

# SETTING UP VERTEX AI
PROJECT_ID = "textdemo-472317"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)

# LOADING GEMININ
model = GenerativeModel("gemini-2.0-flash")

def generate_interview_questions(job_role: str):
    """
    Generate 5 common interview questions for a given job role using Gemini AI.
    Args:
        job_role (str): Target job role
    Returns:
        List[str]: List of interview questions
    """
    prompt = f"Generate 5 common interview questions for a {job_role} role."

    try:
        response = model.generate_content(prompt)
        text_output = response.text.strip()
        questions = [q.strip("-• ") for q in text_output.split("\n") if q.strip()]
        return questions
    except Exception as e:
        print("Error generating questions:", e)
        # FALLBACK HARDCODED QUESTION
        return [
            f"What are the responsibilities of a {job_role}?",
            f"What challenges do you expect in a {job_role} role?",
            "Tell me about a time you solved a problem.",
            "Why do you want this job?",
            "Where do you see yourself in 5 years?"
        ]


