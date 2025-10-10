"""
Webhook para integração com N8N e WhatsApp
Endpoint simplificado para receber mensagens e processar com agentes
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


router = APIRouter(prefix="/webhook", tags=["Webhooks"])


class WhatsAppWebhookRequest(BaseModel):
    """
    Formato esperado do N8N/WAHA
    """
    chat_id: str = Field(..., description="ID do chat (número do WhatsApp)")
    from_number: str = Field(..., alias="from", description="Número do remetente")
    message: str = Field(..., description="Mensagem do usuário")
    message_id: Optional[str] = Field(None, description="ID da mensagem")
    timestamp: Optional[int] = Field(None, description="Timestamp da mensagem")
    pushname: Optional[str] = Field(None, description="Nome do contato no WhatsApp")
    session: Optional[str] = Field("default", description="Sessão WAHA")
    
    class Config:
        populate_by_name = True


class WhatsAppWebhookResponse(BaseModel):
    """
    Resposta formatada para N8N enviar via WAHA
    """
    chat_id: str = Field(..., description="Para quem enviar (mesmo chat_id)")
    message: str = Field(..., description="Resposta do agente")
    session: str = Field(default="default", description="Sessão WAHA")
    agent_used: str = Field(..., description="Qual agente processou")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Dados extras")


@router.post("/whatsapp", response_model=WhatsAppWebhookResponse)
async def whatsapp_webhook(
    request: WhatsAppWebhookRequest,
    background_tasks: BackgroundTasks
):
    """
    🎯 Endpoint principal para receber mensagens do WhatsApp via N8N
    
    **Fluxo:**
    1. N8N recebe mensagem do WAHA
    2. N8N faz POST para este endpoint
    3. Agente processa a mensagem
    4. Retorna resposta formatada
    5. N8N envia resposta via WAHA
    
    **Exemplo de uso no N8N:**
    ```json
    {
      "chat_id": "5511999999999@c.us",
      "from": "5511999999999@c.us",
      "message": "Olá, quero reservar para sábado",
      "pushname": "João Silva",
      "session": "default"
    }
    ```
    """
    print(f"📥 Webhook recebido de {request.pushname} ({request.chat_id}): {request.message}")
    
    try:
        # Cria session_id único para este chat
        session_id = f"whatsapp_{request.chat_id}"
        user_id = request.chat_id
        
        # Contexto adicional
        context = {
            "chat_id": request.chat_id,
            "from": request.from_number,
            "whatsapp_name": request.pushname,
            "session": request.session,
            "timestamp": request.timestamp,
            "message_id": request.message_id,
            "channel": "whatsapp"
        }
        
        from app.agents.host_agent import run as host_run
        
        payload = {
            "message": request.message,
            "user_name": request.pushname or "Cliente",
            "chat_id": request.chat_id,
            "phone": request.from_number,
            "context": context
        }
        
        result = await host_run(payload)
        
        response = WhatsAppWebhookResponse(
            chat_id=request.chat_id,  # Responde para o mesmo chat
            message=result.get("response", "Desculpe, não consegui processar sua mensagem."),
            session=request.session,
            agent_used=result.get("agent", "unknown"),
            metadata={
                "confidence": result.get("confidence"),
                "intent": result.get("intent"),
                "context": result.get("context", {})
            }
        )
        
        print(f"✅ Resposta gerada por agente '{response.agent_used}': {response.message[:50]}...")
        
        background_tasks.add_task(
            save_conversation,
            session_id=session_id,
            user_message=request.message,
            agent_response=response.message,
            context=context
        )
        
        return response
        
    except Exception as e:
        print(f"Erro ao processar webhook: {e}", exc_info=True)
        
        return WhatsAppWebhookResponse(
            chat_id=request.chat_id,
            message="Desculpe, estou com dificuldades técnicas no momento. Por favor, tente novamente em instantes.",
            session=request.session,
            agent_used="error_handler",
            metadata={"error": str(e)}
        )


async def save_conversation(
    session_id: str,
    user_message: str,
    agent_response: str,
    context: Dict[str, Any]
):
    try:
        # TODO: Implementar após configurar banco PostgreSQL
        print(f"💾 Salvando conversa: {session_id}")
        
        
    except Exception as e:
        print(f"Erro ao salvar conversa: {e}")


@router.get("/health")
async def webhook_health():
    return {
        "status": "healthy",
        "service": "whatsapp_webhook",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.post("/test", response_model=WhatsAppWebhookResponse)
async def test_webhook(message: str = "Olá, quero fazer uma reserva"):
    test_request = WhatsAppWebhookRequest(
        chat_id="test_chat_123",
        from_number="5511999999999@c.us",
        message=message,
        pushname="Teste User",
        session="test"
    )
    
    return await whatsapp_webhook(test_request, BackgroundTasks())
