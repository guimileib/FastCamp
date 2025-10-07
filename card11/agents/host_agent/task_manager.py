from common.a2a_client import call_agent
import traceback

FLIGHT_URL = "http://localhost:8001/run"
STAY_URL = "http://localhost:8002/run"
ACTIVITIES_URL = "http://localhost:8003/run"

async def run(payload):
    try:
        # Print what the host agent is sending
        print("=" * 50)
        print("📥 Host Agent - Payload recebido:", payload)
        print("=" * 50)
        
        # Chama os agentes
        print("🔄 Chamando Flight Agent...")
        flights = await call_agent(FLIGHT_URL, payload)
        print("✅ Flight Agent respondeu:", flights)
        
        print("🔄 Chamando Stay Agent...")
        stay = await call_agent(STAY_URL, payload)
        print("✅ Stay Agent respondeu:", stay)
        
        print("🔄 Chamando Activities Agent...")
        activities = await call_agent(ACTIVITIES_URL, payload)
        print("✅ Activities Agent respondeu:", activities)
        
        # Ensure all are dicts before access
        flights = flights if isinstance(flights, dict) else {}
        stay = stay if isinstance(stay, dict) else {}
        activities = activities if isinstance(activities, dict) else {}
        
        result = {
            "flights": flights.get("flights", "Nenhum voo retornado."),
            "stay": stay.get("stays", "Nenhuma hospedagem retornada."),
            "activities": activities.get("activities", "Nenhuma atividade encontrada.")
        }
        
        print("=" * 50)
        print("📤 Host Agent - Resultado final:", result)
        print("=" * 50)
        
        return result
        
    except Exception as e:
        print("=" * 50)
        print("❌ ERRO no Host Agent:")
        print(f"Tipo: {type(e).__name__}")
        print(f"Mensagem: {str(e)}")
        print("Traceback completo:")
        traceback.print_exc()
        print("=" * 50)
        raise

