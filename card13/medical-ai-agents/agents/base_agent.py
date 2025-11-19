import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class BaseAgent:
    def __init__(self, model_name='gemini-2.0-flash'):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY não encontrada no arquivo .env")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def generate(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Erro na geração: {e}"
