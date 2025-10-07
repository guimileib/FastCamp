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

# agente de atividades + instruções do prompt do sistema que orienta o comportamento
activities_agent = Agent(
    name="activities_agent",
    model=LiteLlm("openai/gpt-4o"),
    description="Sugere atividades interessantes para o usuário no destino.",
    instruction=(
        "Dado um destino, datas e orçamento, sugira 2-3 atividades turísticas ou culturais envolventes. "
        "Para cada atividade, forneça nome, descrição curta, estimativa de preço e duração em horas. "
        "Responda em português brasileiro simples. Seja conciso e bem formatado. "
        "IMPORTANTE: Responda SEMPRE em formato JSON válido com a chave 'activities' contendo uma lista de objetos de atividade. "
        "Exemplo: {\"activities\": [{\"nome\": \"Tour pela Torre Eiffel\", \"descricao\": \"Visita guiada\", \"preco\": \"USD 50\", \"duracao\": \"2h\"}]}"
    )
)

# configuração do runner
session_service = InMemorySessionService()
runner = Runner(
    agent=activities_agent,
    app_name="activities_app",
    session_service=session_service
)
USER_ID = "user_activities"
SESSION_ID = "session_activities"

# Execução da lógica, cria um prompt e invoca o modelo e analisa a saída
async def execute(request):
    try:
        print(f"🔄 Activities Agent - Recebendo request: {request}")
        
        destination = request.get('destination', 'Unknown destination')
        start_date = request.get('start_date', 'Unknown date')
        end_date = request.get('end_date', 'Unknown date')
        budget = request.get('budget', 0)
        
        # Simula resposta de atividades melhoradas com links de reserva
        mock_activities = [
            {
                "nome": "Tour pela Torre Eiffel",
                "descricao": "Visita guiada com acesso aos andares superiores e vista panorâmica de Paris",
                "preco": f"R$ {budget * 0.05 * 5.5:.0f}",
                "duracao": "3 horas",
                "categoria": "Turismo Cultural",
                "horario": "09:00 - 12:00",
                "inclui": ["Guia em português", "Acesso aos andares", "Fila prioritária"],
                "link_reserva": "https://www.getyourguide.com.br/paris-l16/torre-eiffel-ingresso-c12/?partner_id=H0IOJ67&utm_medium=online_publisher&placement=content-middle",
                "avaliacao": "4.8/5 ⭐⭐⭐⭐⭐",
                "local_encontro": "Champ de Mars, Paris"
            },
            {
                "nome": "Cruzeiro pelo Rio Sena com Jantar",
                "descricao": "Passeio romântico ao pôr do sol com jantar gourmet e vista dos monumentos",
                "preco": f"R$ {budget * 0.08 * 5.5:.0f}",
                "duracao": "2h30min",
                "categoria": "Experiência Romântica",
                "horario": "19:30 - 22:00",
                "inclui": ["Jantar 3 pratos", "Bebidas", "Música ao vivo", "Guia audiovisual"],
                "link_reserva": "https://www.getyourguide.com.br/paris-l16/cruzeiro-rio-sena-jantar-c89/?partner_id=H0IOJ67&utm_medium=online_publisher&placement=content-middle",
                "avaliacao": "4.6/5 ⭐⭐⭐⭐⭐",
                "local_encontro": "Port de la Bourdonnais, Paris"
            },
            {
                "nome": "Museu do Louvre - Ingresso com Audioguia",
                "descricao": "Visita ao maior museu de arte do mundo com audioguia em português",
                "preco": f"R$ {budget * 0.03 * 5.5:.0f}",
                "duracao": "4 horas",
                "categoria": "Arte e Cultura",
                "horario": "09:00 - 18:00 (flexível)",
                "inclui": ["Ingresso", "Audioguia português", "Mapa do museu", "Fila prioritária"],
                "link_reserva": "https://www.getyourguide.com.br/paris-l16/museu-louvre-ingresso-c67/?partner_id=H0IOJ67&utm_medium=online_publisher&placement=content-middle",
                "avaliacao": "4.7/5 ⭐⭐⭐⭐⭐",
                "local_encontro": "Rue de Rivoli, 75001 Paris"
            },
            {
                "nome": "Tour Gastronômico Montmartre",
                "descricao": "Degustação de queijos, vinhos e doces franceses no charmoso bairro artístico",
                "preco": f"R$ {budget * 0.06 * 5.5:.0f}",
                "duracao": "3h30min",
                "categoria": "Gastronomia",
                "horario": "14:00 - 17:30",
                "inclui": ["Degustações", "Guia local", "História do bairro", "Vinhos franceses"],
                "link_reserva": "https://www.getyourguide.com.br/paris-l16/tour-gastronomico-montmartre-c45/?partner_id=H0IOJ67&utm_medium=online_publisher&placement=content-middle",
                "avaliacao": "4.9/5 ⭐⭐⭐⭐⭐",
                "local_encontro": "Place du Tertre, Montmartre",
                "promocao": "🍷 EXPERIÊNCIA ÚNICA!"
            }
        ]
        
        print(f"✅ Activities Agent - Retornando: {mock_activities}")
        return {"activities": mock_activities}
        
    except Exception as e:
        print(f"❌ Erro no Activities Agent: {e}")
        return {"activities": f"Erro: {str(e)}"}  