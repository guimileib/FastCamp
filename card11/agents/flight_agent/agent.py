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

# agente de voos + instruções do prompt do sistema que orienta o comportamento
flight_agent = Agent(
    name="flight_agent",
    model=LiteLlm("openai/gpt-4o"),
    description="Encontra opções de voos adequadas para o plano de viagem do usuário.",
    instruction=(
        "Dado uma origem, destino, data de ida, data de volta e orçamento, sugira 2-3 opções de voos. "
        "Para cada voo, forneça nome da companhia aérea, horário de partida, horário de chegada, duração e preço estimado. "
        "Responda em português brasileiro simples. Seja conciso e bem formatado. "
        "IMPORTANTE: Responda SEMPRE em formato JSON válido com a chave 'flights' contendo uma lista de objetos de voo. "
        "Exemplo: {\"flights\": [{\"companhia\": \"LATAM\", \"partida\": \"08:00\", \"chegada\": \"12:00\", \"duracao\": \"4h\", \"preco\": \"USD 500\"}]}"
    )
)

# configuração do runner
session_service = InMemorySessionService()
runner = Runner(
    agent=flight_agent,
    app_name="flight_app",
    session_service=session_service
)
USER_ID = "user_flights"
SESSION_ID = "session_flights"

# Execução da lógica, cria um prompt e invoca o modelo e analisa a saída
async def execute(request):
    try:
        print(f"🔄 Flight Agent - Recebendo request: {request}")
        
        origin = request.get('origin', 'Unknown origin')
        destination = request.get('destination', 'Unknown destination')
        start_date = request.get('start_date', 'Unknown date')
        end_date = request.get('end_date', 'Unknown date')
        budget = request.get('budget', 0)
        
        # Simula resposta de voos com links diretos de compra e ida/volta
        origin_encoded = origin.replace(" ", "%20")
        destination_encoded = destination.replace(" ", "%20")
        
        mock_flights = [
            {
                "tipo": "IDA",
                "companhia": "LATAM",
                "partida": "08:00",
                "chegada": "22:30", 
                "duracao": "14h30m",
                "preco": f"R$ {budget * 0.3 * 5.5:.0f}",
                "rota": f"{origin} → {destination}",
                "link_compra": f"https://www.latam.com/pt_br/apps/personas?fecha1_dia={start_date.split('-')[2]}&fecha1_anomes={start_date.split('-')[1]}{start_date.split('-')[0]}&from_city1={origin_encoded}&to_city1={destination_encoded}&auAvailability=1&ida_vuelta=ida&tipo_pasajero1=ADT&cantidad_pasajeros=1&cantidad_ninos=0&cantidad_infantes=0",
                "codigo_voo": "LA8084",
                "classe": "Econômica"
            },
            {
                "tipo": "IDA", 
                "companhia": "Air France",
                "partida": "14:20",
                "chegada": "06:45+1",
                "duracao": "16h25m", 
                "preco": f"R$ {budget * 0.4 * 5.5:.0f}",
                "rota": f"{origin} → {destination}",
                "link_compra": f"https://wwws.airfrance.com.br/search/open-dates?pax=1:0:0:0:0:0:0:0&cabinClass=ECONOMY&activeConnection=0&connections={origin_encoded}:{destination_encoded}:{start_date}",
                "codigo_voo": "AF459",
                "classe": "Econômica"
            },
            {
                "tipo": "IDA",
                "companhia": "Azul",
                "partida": "23:45",
                "chegada": "18:20+1",
                "duracao": "18h35m", 
                "preco": f"R$ {budget * 0.25 * 5.5:.0f}",
                "rota": f"{origin} → {destination}",
                "link_compra": f"https://www.voeazul.com.br/pt/informacoes/reservas?origin={origin_encoded}&destination={destination_encoded}&departureDate={start_date}&returnDate=&tripType=ONE_WAY&adults=1&children=0&infants=0",
                "codigo_voo": "AD7894",
                "classe": "Econômica",
                "promocao": "🔥 MELHOR PREÇO!"
            },
            {
                "tipo": "VOLTA",
                "companhia": "LATAM",
                "partida": "10:15",
                "chegada": "16:45",
                "duracao": "12h30m",
                "preco": f"R$ {budget * 0.28 * 5.5:.0f}",
                "rota": f"{destination} → {origin}",
                "link_compra": f"https://www.latam.com/pt_br/apps/personas?fecha1_dia={end_date.split('-')[2]}&fecha1_anomes={end_date.split('-')[1]}{end_date.split('-')[0]}&from_city1={destination_encoded}&to_city1={origin_encoded}&auAvailability=1&ida_vuelta=ida&tipo_pasajero1=ADT&cantidad_pasajeros=1&cantidad_ninos=0&cantidad_infantes=0",
                "codigo_voo": "LA8185",
                "classe": "Econômica"
            },
            {
                "tipo": "VOLTA",
                "companhia": "Air France", 
                "partida": "16:30",
                "chegada": "09:20+1",
                "duracao": "14h50m",
                "preco": f"R$ {budget * 0.35 * 5.5:.0f}",
                "rota": f"{destination} → {origin}",
                "link_compra": f"https://wwws.airfrance.com.br/search/open-dates?pax=1:0:0:0:0:0:0:0&cabinClass=ECONOMY&activeConnection=0&connections={destination_encoded}:{origin_encoded}:{end_date}",
                "codigo_voo": "AF460",
                "classe": "Econômica"
            },
            {
                "tipo": "VOLTA",
                "companhia": "Azul",
                "partida": "22:10", 
                "chegada": "14:55+1",
                "duracao": "16h45m",
                "preco": f"R$ {budget * 0.22 * 5.5:.0f}",
                "rota": f"{destination} → {origin}",
                "link_compra": f"https://www.voeazul.com.br/pt/informacoes/reservas?origin={destination_encoded}&destination={origin_encoded}&departureDate={end_date}&returnDate=&tripType=ONE_WAY&adults=1&children=0&infants=0",
                "codigo_voo": "AD7895",
                "classe": "Econômica",
                "promocao": "💰 VOLTA ECONÔMICA!"
            }
        ]
        
        print(f"✅ Flight Agent - Retornando: {mock_flights}")
        return {"flights": mock_flights}
        
    except Exception as e:
        print(f"❌ Erro no Flight Agent: {e}")
        return {"flights": f"Erro: {str(e)}"}
