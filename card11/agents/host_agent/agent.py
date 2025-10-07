from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()
if not os.getenv('OPENAI_API_KEY'):
    raise ValueError("OPENAI_API_KEY não encontrada! Configure o arquivo .env")


host_agent = Agent(
    name="host_agent",
    model=LiteLlm("openai/gpt-4o"),
    description="Coordena o planejamento de viagens chamando os agentes de voo, hospedagem e atividades.",
    instruction="Você é o agente host responsável por orquestrar as tarefas de planejamento de viagem. "
                "Você chama agentes externos para coletar voos, hospedagens e atividades, e então retorna um resultado final em português brasileiro."
)
session_service = InMemorySessionService()
runner = Runner(
    agent=host_agent,
    app_name="host_app",
    session_service=session_service
)
USER_ID = "user_host"
SESSION_ID = "session_host"

async def execute(request):
    try:
        print(f"🔄 Host Agent - Recebendo request: {request}")
        
        origin = request.get('origin', 'Unknown origin')
        destination = request.get('destination', 'Unknown destination')
        start_date = request.get('start_date', 'Unknown date')
        end_date = request.get('end_date', 'Unknown date')
        budget = request.get('budget', 0)
        
        # Simulação de resposta coordenada de todos os agentes
        coordinated_response = {
            "flights": [
                {
                    "tipo": "IDA",
                    "companhia": "LATAM",
                    "partida": "08:00",
                    "chegada": "22:30", 
                    "duracao": "14h30m",
                    "preco": f"R$ {budget * 0.3 * 5.5:.0f}",
                    "rota": f"{origin} → {destination}",
                    "link_compra": f"https://www.latam.com/pt_br/apps/personas?fecha1_dia={start_date.split('-')[2]}&fecha1_anomes={start_date.split('-')[1]}{start_date.split('-')[0]}&from_city1={origin.replace(' ', '%20')}&to_city1={destination.replace(' ', '%20')}&auAvailability=1&ida_vuelta=ida&tipo_pasajero1=ADT&cantidad_pasajeros=1&cantidad_ninos=0&cantidad_infantes=0",
                    "codigo_voo": "LA8084",
                    "classe": "Econômica"
                },
                {
                    "tipo": "VOLTA",
                    "companhia": "LATAM",
                    "partida": "10:15",
                    "chegada": "16:45",
                    "duracao": "12h30m",
                    "preco": f"R$ {budget * 0.28 * 5.5:.0f}",
                    "rota": f"{destination} → {origin}",
                    "link_compra": f"https://www.latam.com/pt_br/apps/personas?fecha1_dia={end_date.split('-')[2]}&fecha1_anomes={end_date.split('-')[1]}{end_date.split('-')[0]}&from_city1={destination.replace(' ', '%20')}&to_city1={origin.replace(' ', '%20')}&auAvailability=1&ida_vuelta=ida&tipo_pasajero1=ADT&cantidad_pasajeros=1&cantidad_ninos=0&cantidad_infantes=0",
                    "codigo_voo": "LA8185",
                    "classe": "Econômica"
                }
            ],
            "stays": [
                {
                    "nome": "Hotel Mercure Paris Centre",
                    "localizacao": "Centro de Paris - Châtelet",
                    "tipo_quarto": "Standard Double",
                    "preco_noite": f"R$ {budget * 0.15 * 5.5:.0f}",
                    "preco_total": f"R$ {budget * 0.6 * 5.5:.0f}",
                    "avaliacao": "4.2/5 ⭐⭐⭐⭐",
                    "link_reserva": "https://www.booking.com/hotel/fr/mercure-paris-centre.pt-br.html",
                    "comodidades": ["Wi-Fi gratuito", "Academia", "Restaurante", "Room Service"],
                    "cancelamento": "Cancelamento grátis até 24h antes"
                }
            ],
            "activities": [
                {
                    "nome": "Tour pela Torre Eiffel",
                    "descricao": "Visita guiada com acesso aos andares superiores e vista panorâmica de Paris",
                    "preco": f"R$ {budget * 0.05 * 5.5:.0f}",
                    "duracao": "3 horas",
                    "categoria": "Turismo Cultural",
                    "horario": "09:00 - 12:00",
                    "inclui": ["Guia em português", "Acesso aos andares", "Fila prioritária"],
                    "link_reserva": "https://www.getyourguide.com.br/paris-l16/torre-eiffel-ingresso-c12/",
                    "avaliacao": "4.8/5 ⭐⭐⭐⭐⭐",
                    "local_encontro": "Champ de Mars, Paris"
                }
            ]
        }
        
        print(f"✅ Host Agent - Retornando resposta coordenada completa")
        return coordinated_response
        
    except Exception as e:
        print(f"❌ Erro no Host Agent: {e}")
        return {"error": f"Erro: {str(e)}"}