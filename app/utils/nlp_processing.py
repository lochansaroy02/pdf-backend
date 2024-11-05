# app/utils/nlp_processing.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
from jinja2 import Template

# Load environment variables from .env file
load_dotenv()

# Configure Google Generative AI with API key from environment variable
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])


def answer_question(pdf_text: str, question: str) -> str:
    # Initialize the model
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Create the Jinja template and render it with the provided variables
    template = Template(
        "Answer the question based on the text:\n\n{{ pdf_text }}\n\nQuestion: {{ question }}")
    prompt = template.render(pdf_text=pdf_text, question=question)

    # Generate response from the model
    response = model.generate_content(prompt)

    # Return the generated answer text
    return response.text.strip()
