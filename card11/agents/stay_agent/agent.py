from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import json
from dotenv import load_dotenv
import os

load_dotenv()
if not os.getenv('OPENAI_API_KEY'):
    raise ValueError("OPENAI_API_KEY não encontrada! Configure o arquivo .env")

# agente de hospedagem + instruções do prompt do sistema que orienta o comportamento
stay_agent = Agent(
    name="stay_agent",
    model=LiteLlm("openai/gpt-4o"),
    description="Sugere opções de acomodação adequadas para a viagem do usuário.",
    instruction=(
        "Dado um destino, data de check-in, data de check-out e orçamento, sugira 2-3 opções de hospedagem. "
        "Para cada opção, forneça nome do hotel/propriedade, localização, tipo de quarto, preço por noite e preço total. "
        "Responda em português brasileiro simples. Seja conciso e bem formatado. "
        "IMPORTANTE: Responda SEMPRE em formato JSON válido com a chave 'stays' contendo uma lista de objetos de hospedagem. "
        "Exemplo: {\"stays\": [{\"nome\": \"Hotel Exemplo\", \"localizacao\": \"Centro\", \"tipo_quarto\": \"Standard\", \"preco_noite\": \"USD 80\", \"preco_total\": \"USD 240\"}]}"
    )
)

# configuração do runner
session_service = InMemorySessionService()
runner = Runner(
    agent=stay_agent,
    app_name="stay_app",
    session_service=session_service
)
USER_ID = "user_stays"
SESSION_ID = "session_stays"

# Execução da lógica, cria um prompt e invoca o modelo e analisa a saída
async def execute(request):
    try:
        print(f"🔄 Stay Agent - Recebendo request: {request}")
        
        destination = request.get('destination', 'Unknown destination')
        start_date = request.get('start_date', 'Unknown date')
        end_date = request.get('end_date', 'Unknown date')
        budget = request.get('budget', 0)
        
        # Simula resposta de hospedagens com links de reserva em Real
        mock_stays = [
            {
                "nome": "Hotel Mercure Paris Centre",
                "localizacao": "Centro de Paris - Châtelet",
                "tipo_quarto": "Standard Double",
                "preco_noite": f"R$ {budget * 0.15 * 5.5:.0f}",
                "preco_total": f"R$ {budget * 0.6 * 5.5:.0f}",
                "avaliacao": "4.2/5 ⭐⭐⭐⭐",
                "link_reserva": "https://www.booking.com/hotel/fr/mercure-paris-centre.pt-br.html?aid=356980&label=gog235jc-1DCAsonQFCCm1lcmN1cmUtcGFyaXNIM1gDbKEBiAEBmAEJuAEXyAEP2AED6AEB-AECiAIBqAIDuAKvyY-0BsACAdICJGZkOGExNDY4LTdhOWMtNDVmNy04YWM5LTAzMzRmNjc2OGQ5OdgCBOACAQ&sid=d8ff18e2b5b9ff2e69b8d5a0cbf72df0",
                "comodidades": ["Wi-Fi gratuito", "Academia", "Restaurante", "Room Service"],
                "cancelamento": "Cancelamento grátis até 24h antes"
            },
            {
                "nome": "Ibis Budget Paris Louvre",
                "localizacao": "Próximo ao Louvre - 1º Arrondissement", 
                "tipo_quarto": "Economy Room",
                "preco_noite": f"R$ {budget * 0.08 * 5.5:.0f}",
                "preco_total": f"R$ {budget * 0.35 * 5.5:.0f}",
                "avaliacao": "3.8/5 ⭐⭐⭐",
                "link_reserva": "https://www.booking.com/hotel/fr/ibis-budget-paris-porte-de-montmartre.pt-br.html?aid=356980&label=gog235jc-1DCAsonQFCDGliaXMtYnVkZ2V0SAtYA2yhAYgBAZgBCbgBF8gBD9gBA-gBAagCBbgCr8mPtAbAAgHSAiRmZDhhMTQ2OC03YTljLTQ1ZjctOGFjOS0wMzM0ZjY3NjhkOTXYAgTgAgE&sid=d8ff18e2b5b9ff2e69b8d5a0cbf72df0",
                "comodidades": ["Wi-Fi gratuito", "Ar condicionado", "Recepção 24h"],
                "cancelamento": "Cancelamento grátis",
                "promocao": "💰 ECONÔMICO"
            },
            {
                "nome": "Hotel des Grands Boulevards",
                "localizacao": "Grands Boulevards - 2º Arrondissement",
                "tipo_quarto": "Superior Room",
                "preco_noite": f"R$ {budget * 0.25 * 5.5:.0f}",
                "preco_total": f"R$ {budget * 0.8 * 5.5:.0f}",
                "avaliacao": "4.6/5 ⭐⭐⭐⭐⭐",
                "link_reserva": "https://www.booking.com/hotel/fr/des-grands-boulevards.pt-br.html?aid=356980&label=gog235jc-1DCAsonQFCFGRlcy1ncmFuZHMtYm91bGV2YXJkcxgESDNYA2yhAYgBAZgBCbgBF8gBD9gBA-gBAagCBbgCr8mPtAbAAgHSAiRmZDhhMTQ2OC03YTljLTQ1ZjctOGFjOS0wMzM0ZjY3NjhkOTXYAgTgAgE&sid=d8ff18e2b5b9ff2e69b8d5a0cbf72df0",
                "comodidades": ["Wi-Fi gratuito", "Spa", "Bar", "Restaurante gourmet", "Terraço"],
                "cancelamento": "Flexível",
                "promocao": "🌟 LUXO"
            }
        ]
        
        print(f"✅ Stay Agent - Retornando: {mock_stays}")
        return {"stays": mock_stays}
        
    except Exception as e:
        print(f"❌ Erro no Stay Agent: {e}")
        return {"stays": f"Erro: {str(e)}"}
