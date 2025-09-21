# utils/career_info.py
import streamlit as st
import vertexai
from vertexai.generative_models import GenerativeModel

# VERTEX AI MODEL SETUP
PROJECT_ID = "textdemo-472317"
LOCATION = "us-central1"
vertexai.init(project=PROJECT_ID, location=LOCATION)
model = GenerativeModel("gemini-2.0-flash")


# FUNCTION TO FETCH INFORMATION ABOUT CAREEN
def fetch_career_information(career_role: str):

    if not career_role.strip():
        st.warning("Please enter a career role.")
        return

    st.info(f"Fetching information about {career_role}...")

    # SETTING UP PROMPTS TO GET OVERVIEW,COMPANIES,TOOLS AND TECH AND LATEST DEVELOPMENT
    prompts = {
        "overview": f"Provide a brief overview of the career: {career_role}.",
        "companies": f"List the top companies that hire for the career: {career_role}.",
        "tools_tech": f"List the main tools and technologies required for the career: {career_role}.",
        "developments": f"Mention any latest developments, news, or trends in the career field: {career_role}."
    }

    # DICTIONARY TO STORE INFORMATION
    responses = {}

    try:
        for key, prompt in prompts.items():
            response = model.generate_content(prompt)
            responses[key] = response.text.strip()

        # DISPLAYING EACH SECTION IN DIFFERENT BOXES
        with st.expander("Career Overview", expanded=True):
            st.markdown(responses.get("overview", "No overview available."))

        with st.expander("Top Companies", expanded=True):
            st.markdown(responses.get("companies", "No company information available."))

        with st.expander("Tools & Technologies", expanded=True):
            st.markdown(responses.get("tools_tech", "No tools/technologies information available."))

        with st.expander("Latest Developments", expanded=True):
            st.markdown(responses.get("developments", "No developments information available."))

    except Exception as e:
        st.error(f"Error fetching career information: {e}")

        # Fallback content
        with st.expander("Career Overview", expanded=True):
            st.markdown(f"{career_role} is a specialized career with growing demand.")

        with st.expander("Top Companies", expanded=True):
            st.markdown("- Example Corp\n- Tech Innovations\n- Global Solutions")

        with st.expander("Tools & Technologies", expanded=True):
            st.markdown("- Tool1\n- Tool2\n- Tool3")

        with st.expander("Latest Developments", expanded=True):
            st.markdown("- Development1\n- Development2\n- Development3")


