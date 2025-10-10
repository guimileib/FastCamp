from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from app.routes import agents_routes

load_dotenv()

WHATSAPP_PHONE = os.getenv("WHATSAPP_PHONE_NUMBER")
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
API_DEBUG = os.getenv("API_DEBUG", "true").lower() == "true"


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("=" * 60)
    print("Iniciando Party Agent API (Google ADK)")
    print("=" * 60)
    print(f"WhatsApp: {WHATSAPP_PHONE}")
    print(f"N8N Webhook: {N8N_WEBHOOK_URL}")
    print(f"API Host: {API_HOST}:{API_PORT}")
    print("\nEndpoints disponíveis:")
    print("   - POST /webhook/whatsapp  (N8N Integration)")
    print("   - POST /agents/maria      (Maria Agent - ADK)")
    print("   - POST /agents/booking    (Booking Agent - ADK)")
    print("   - POST /agents/report     (Report Agent - ADK)")
    print("   - POST /agents/host       (Host Orchestrator - ADK)")
    print("   - GET  /agents/           (Lista todos os agentes)")
    print("=" * 60)
    
    yield
    
    print("\n👋 Encerrando Party Agent...")


app = FastAPI(
    title="Party Agent API",
    description="""
    API do Agente de Atendimento para Espaço de Festa integrado com WhatsApp via N8N.
    
    ## Funcionalidades
    
    * **Atendimento Automatizado**: Responde perguntas sobre o espaço de festa
    * **Verificação de Disponibilidade**: Consulta datas disponíveis
    * **Criação de Reservas**: Coleta informações e cria reservas
    * **Integração WhatsApp**: Conectado via N8N para automações
    * **Gerenciamento de Sessões**: Mantém histórico de conversas
    * **Evaluation Sets**: Sistema de avaliação e métricas
    * **Debug e Tracing**: Ferramentas para depuração
    
    ## Integrações
    
    * **N8N**: Webhooks e automações
    * **WhatsApp Business**: Atendimento via mensagens
    * **ADK**: Agent Development Kit para IA conversacional
    
    ## Sistema Multi-Agente
    
    * **Agente de Atendimento**: Reservas, preços, informações
    * **Agente de Agendamento**: Visualizar datas, calendário, sugestões
    * **Agente de Analytics**: Relatórios, métricas, análises
    * **Agente Administrativo**: Configurações, cancelamentos, gestão
    """,
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(agents_routes.router, tags=["Agents (ADK)"])

try:
    app.mount("/static", StaticFiles(directory="static"), name="static")
except Exception as e:
    print(f"Não foi possível montar diretório static: {e}")

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "agent": "Party Agent",
        "n8n_configured": bool(N8N_WEBHOOK_URL)
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=API_DEBUG
    )
