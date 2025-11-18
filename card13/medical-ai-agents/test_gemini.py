import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("API não encontrada no arquivo .env")

genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-2.0-flash-exp')

try:
    response = model.generate_content("Diga olá em português")
    print("API funcionando!")
    print(f"Resposta: {response.text}")
except Exception as e:
    print(f"Erro: {e}")