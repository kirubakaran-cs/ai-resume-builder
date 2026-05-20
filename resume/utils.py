import google.generativeai as genai
from django.conf import settings


def generate_ai_summary(resume_data: dict) -> str:
    """
    Sends resume data to Google Gemini and returns a professional summary.

    Args:
        resume_data: A dictionary with keys like name, skills, experience, etc.

    Returns:
        A string with the AI-generated professional summary.
    """
    try:
        # Configure the Gemini API with our key
        genai.configure(api_key=settings.GEMINI_API_KEY)

        # Use the free Gemini Flash model
        model = genai.GenerativeModel('gemini-1.5-flash')

        # Build a detailed prompt for the AI
        prompt = f"""
        You are a professional resume writer. Write a compelling 3-4 sentence
        professional summary for a resume based on the following information.
        Make it concise, impactful, and written in first person.
        Do NOT include a heading like "Professional Summary:".

        Name: {resume_data.get('full_name', '')}
        Skills: {resume_data.get('skills', '')}
        Experience: {resume_data.get('experience', '')}
        Education: {resume_data.get('education', '')}
        Projects: {resume_data.get('projects', '')}

        Write only the summary paragraph, nothing else.
        """

        response = model.generate_content(prompt)
        return response.text.strip()

    except Exception as e:
        # If AI fails, return a generic message (don't crash the app!)
        print(f"Gemini API error: {e}")
        return "A dedicated professional with strong technical skills and a passion for creating impactful solutions."