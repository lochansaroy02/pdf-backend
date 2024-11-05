# app/utils/nlp_processing.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain.prompts import PromptTemplate

# Load environment variables from .env file
load_dotenv()

# Configure Google Generative AI with API key from environment variable
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def answer_question(pdf_text: str, question: str) -> str:
    # Initialize the model
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Create a prompt template
    prompt_template = PromptTemplate(
        input_variables=["pdf_text", "question"],
        template="Answer the question based on the text:\n\n{pdf_text}\n\nQuestion: {question}"
    )
    prompt = prompt_template.format(pdf_text=pdf_text, question=question)

    # Generate response from the model
    response = model.generate_content(prompt)

    # Return the generated answer text
    return response.text.strip()
