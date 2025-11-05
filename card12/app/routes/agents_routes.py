from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List


router = APIRouter(prefix="/agents", tags=["Agents (ADK)"])


class AgentRequest(BaseModel):
    message: str = Field(..., description="Mensagem do usuário")
    user_id: str = Field(..., description="ID do usuário (chat_id)")
    user_name: str = Field(default="Cliente", description="Nome do usuário")
    session_id: Optional[str] = Field(None, description="ID da sessão")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Metadados extras")
    history: Optional[List[Dict[str, str]]] = Field(default_factory=list, description="Histórico de conversa")


class AgentResponse(BaseModel):
    response: str = Field(..., description="Resposta do agente")
    agent: str = Field(..., description="Nome do agente que processou")
    confidence: float = Field(..., description="Confiança da resposta (0-1)")
    events: List[Dict[str, Any]] = Field(default_factory=list, description="Eventos emitidos")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadados da resposta")
    tools_used: List[str] = Field(default_factory=list, description="Tools utilizadas")


@router.post("/maria", response_model=AgentResponse)
async def maria_agent_endpoint(request: AgentRequest):
    print(f"Endpoint /agents/maria chamado por {request.user_name}")
    
    try:
        from app.agents.maria_agent.agent import maria_agent
        
        payload = {
            "message": request.message,
            "user_id": request.user_id,
            "user_name": request.user_name,
            "session_id": request.session_id,
            "metadata": request.metadata,
            "history": request.history
        }
        
        result = await maria_agent.run(payload)
        
        return AgentResponse(
            response=result["response"],
            agent=result["agent"],
            confidence=result.get("confidence", 0.85),
            events=result.get("events", []),
            metadata=result.get("metadata", {}),
            tools_used=result.get("tools_used", [])
        )
    
    except Exception as e:
        print(f"Erro no endpoint Maria: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar com Maria Agent: {str(e)}")


@router.post("/booking", response_model=AgentResponse)
async def booking_agent_endpoint(request: AgentRequest):
    print(f"Endpoint /agents/booking chamado por {request.user_name}")
    
    try:
        from app.agents.booking_agent.agent import booking_agent
        
        payload = {
            "message": request.message,
            "user_id": request.user_id,
            "user_name": request.user_name,
            "session_id": request.session_id,
            "metadata": request.metadata,
            "history": request.history,
            "chat_id": request.user_id,
            "phone": request.metadata.get("phone", request.user_id.split('@')[0] if '@' in request.user_id else request.user_id)
        }
        
        result = await booking_agent.run(payload)
        
        return AgentResponse(
            response=result["response"],
            agent=result["agent"],
            confidence=result.get("confidence", 0.85),
            events=result.get("events", []),
            metadata=result.get("metadata", {}),
            tools_used=result.get("tools_used", [])
        )
    
    except Exception as e:
        print(f"Erro no endpoint Booking: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar com Booking Agent: {str(e)}")


@router.post("/report", response_model=AgentResponse)
async def report_agent_endpoint(request: AgentRequest):
    print(f"Endpoint /agents/report chamado por {request.user_name}")
    
    try:
        from app.agents.report_agent.agent import execute as report_execute
        
        payload = {
            "message": request.message,
            "user_name": request.user_name,
            "chat_id": request.user_id,
            "phone": request.metadata.get("phone", ""),
            "context": request.metadata
        }
        
        result = await report_execute(payload)
        
        return AgentResponse(
            response=result.get("response", "Relatório processado"),
            agent=result.get("agent", "report_agent"),
            confidence=result.get("confidence", 0.9),
            events=[],
            metadata=result,
            tools_used=[]
        )
    
    except Exception as e:
        print(f"Erro no endpoint Report: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar com Report Agent: {str(e)}")


@router.post("/host", response_model=AgentResponse)
async def host_agent_endpoint(request: AgentRequest):
    print(f"Endpoint /agents/host chamado por {request.user_name}")
    
    try:
        from app.agents.host_agent.agent import execute as host_execute
        
        payload = {
            "message": request.message,
            "user_name": request.user_name,
            "chat_id": request.user_id,
            "phone": request.metadata.get("phone", request.user_id.split('@')[0] if '@' in request.user_id else request.user_id),
            "context": request.metadata,
            "conversation_history": request.history or []
        }
        
        result = await host_execute(payload)
        
        # O host agent retorna o resultado do agente escolhido
        return AgentResponse(
            response=result.get("message", result.get("response", "")),
            agent=result.get("orchestrator", {}).get("chosen_agent", "host_agent"),
            confidence=result.get("orchestrator", {}).get("confidence", 0.7),
            events=[],
            metadata={
                "orchestrator": result.get("orchestrator", {}),
                "report_sent": result.get("report_sent", False),
                "original_result": result
            },
            tools_used=[]
        )
    
    except Exception as e:
        print(f"Erro no endpoint Host: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao processar com Host Agent: {str(e)}")

# a partir das listas de agentes retorna informações sobre cada agente e seus endpoints
@router.get("/") 
async def list_agents():
    return {
        "agents": [
            {
                "name": "maria_agent",
                "endpoint": "/agents/maria",
                "description": "Agente de atendimento e qualificação de leads",
                "capabilities": [
                    "Saudações e atendimento inicial",
                    "Informações sobre o espaço",
                    "Qualificação de leads",
                    "Respostas personalizadas"
                ]
            },
            {
                "name": "booking_agent",
                "endpoint": "/agents/booking",
                "description": "Agente de agendamento e reservas",
                "capabilities": [
                    "Extração de data/horário/convidados",
                    "Criação de reservas no Supabase",
                    "Confirmação de agendamentos",
                    "Validação de informações"
                ]
            },
            {
                "name": "report_agent",
                "endpoint": "/agents/report",
                "description": "Agente de relatórios e notificações",
                "capabilities": [
                    "Geração de relatórios",
                    "Envio de notificações",
                    "Resumo de conversas",
                    "Alertas para empresa"
                ]
            },
            {
                "name": "host_agent",
                "endpoint": "/agents/host",
                "description": "Orquestrador de agentes (roteamento inteligente)",
                "capabilities": [
                    "Classificação de mensagens",
                    "Roteamento para agentes",
                    "Coordenação multi-agente",
                    "Gerenciamento de fluxo"
                ]
            }
        ],
        "architecture": "Google ADK (Agent Development Kit)",
        "port": 8000,
        "version": "2.0.0"
    }
