from fastapi import APIRouter, HTTPException, Depends
from typing import Optional, Dict, Any

from app.models.session import Message, SessionCreate, SessionResponse
from app.models.agent import AgentRunRequest, AgentRunResponse
from app.agents.base_agent import AgentType
from app.agents.agent_router import get_router
from app.services.n8n_service import N8NService


router = APIRouter(prefix="/api/v1/agents", tags=["Multi-Agent System"])

def get_n8n_service():
    return N8NService()


@router.post("/route", response_model=Dict[str, Any])
async def route_to_agent(
    message: str,
    session_id: str,
    user_id: str = "default_user",
    agent_type: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
    n8n_service: N8NService = Depends(get_n8n_service)
):
    """
    REstrutura
    
    - **message**: Mensagem do usuário
    - **session_id**: ID da sessão
    - **user_id**: ID do usuário (opcional)
    - **agent_type**: Tipo de agente (opcional, auto-detecta se omitido)
    - **context**: Contexto adicional (opcional)
    """
    router_instance = get_router(n8n_service)
    
    # Converte string para enum se fornecido
    agent_enum = None
    if agent_type:
        try:
            agent_enum = AgentType(agent_type)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de agente inválido: {agent_type}"
            )
    
    try:
        response = await router_instance.route_message(
            message=message,
            session_id=session_id,
            user_id=user_id,
            agent_type=agent_enum,
            context=context
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{agent_type}/run", response_model=Dict[str, Any])
async def run_specific_agent(
    agent_type: str,
    message: str,
    session_id: str,
    user_id: str = "default_user",
    context: Optional[Dict[str, Any]] = None,
    n8n_service: N8NService = Depends(get_n8n_service)
):
    """
    Estrutura:
    - **agent_type**: attendance, schedule, analytics, ou admin
    - **message**: Mensagem do usuário
    - **session_id**: ID da sessão
    - **user_id**: ID do usuário (opcional)
    - **context**: Contexto adicional (opcional)
    """
    try:
        agent_enum = AgentType(agent_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de agente inválido: {agent_type}. Use: attendance, schedule, analytics, admin"
        )
    
    router_instance = get_router(n8n_service)
    agent = router_instance.get_agent(agent_enum)
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agente não encontrado")
    
    try:
        response = await agent.process_message(
            message=message,
            session_id=session_id,
            user_id=user_id,
            context=context
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/capabilities", response_model=Dict[str, Any])
async def get_all_capabilities(
    n8n_service: N8NService = Depends(get_n8n_service)
):
    router_instance = get_router(n8n_service)
    return router_instance.get_all_capabilities()


@router.get("/{agent_type}/info", response_model=Dict[str, Any])
async def get_agent_info(
    agent_type: str,
    n8n_service: N8NService = Depends(get_n8n_service)
):
    try:
        agent_enum = AgentType(agent_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de agente inválido: {agent_type}"
        )
    
    router_instance = get_router(n8n_service)
    info = router_instance.get_agent_info(agent_enum)
    
    if "error" in info:
        raise HTTPException(status_code=404, detail=info["error"])
    
    return info


@router.post("/suggest", response_model=Dict[str, Any])
async def suggest_agent(
    message: str,
    n8n_service: N8NService = Depends(get_n8n_service)
):
    router_instance = get_router(n8n_service)
    return router_instance.suggest_agent(message)


@router.get("/types", response_model=Dict[str, Any])
async def list_agent_types():
    return {
        "agent_types": [
            {
                "type": "attendance",
                "name": "Agente de Atendimento",
                "description": "Atendimento ao cliente, reservas, preços"
            },
            {
                "type": "schedule",
                "name": "Agente de Agendamento",
                "description": "Visualizar datas, agenda, disponibilidade"
            },
            {
                "type": "analytics",
                "name": "Agente de Analytics",
                "description": "Relatórios, métricas, análise de dados"
            },
            {
                "type": "admin",
                "name": "Agente Administrativo",
                "description": "Configurações, cancelamentos, gestão"
            }
        ]
    }


#endpoints específicos por agente 
@router.post("/attendance/check-availability")
async def attendance_check_availability(
    date: str,
    period: str = "noite",
    guest_count: Optional[int] = None,
    n8n_service: N8NService = Depends(get_n8n_service)
):
    router_instance = get_router(n8n_service)
    agent = router_instance.get_agent(AgentType.ATTENDANCE)
    
    try:
        result = await agent.check_availability(date, period, guest_count)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/attendance/create-booking")
async def attendance_create_booking(
    date: str,
    customer_name: str,
    customer_phone: str,
    event_type: str,
    guest_count: int,
    n8n_service: N8NService = Depends(get_n8n_service)
):
    router_instance = get_router(n8n_service)
    agent = router_instance.get_agent(AgentType.ATTENDANCE)
    
    try:
        result = await agent.create_booking(
            date, customer_name, customer_phone, event_type, guest_count
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/schedule/calendar")
async def schedule_view_calendar(
    start_date: str,
    end_date: str,
    n8n_service: N8NService = Depends(get_n8n_service)
):
    router_instance = get_router(n8n_service)
    agent = router_instance.get_agent(AgentType.SCHEDULE)
    
    try:
        result = await agent.view_calendar(start_date, end_date)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analytics/stats")
async def analytics_booking_stats(
    start_date: str,
    end_date: str,
    group_by: str = "day",
    n8n_service: N8NService = Depends(get_n8n_service)
):
    router_instance = get_router(n8n_service)
    agent = router_instance.get_agent(AgentType.ANALYTICS)
    
    try:
        result = agent.get_booking_stats(start_date, end_date, group_by)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/admin/cancel-booking")
async def admin_cancel_booking(
    booking_id: str,
    reason: str,
    refund_amount: Optional[float] = None,
    n8n_service: N8NService = Depends(get_n8n_service)
):
    router_instance = get_router(n8n_service)
    agent = router_instance.get_agent(AgentType.ADMIN)
    
    try:
        result = await agent.cancel_booking(booking_id, reason, refund_amount)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
