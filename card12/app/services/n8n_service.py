import httpx
from typing import Dict, Any, Optional
from datetime import datetime
from loguru import logger

from config.settings import settings
from app.models.n8n import (
    BookingRequest, BookingResponse,
    AvailabilityCheck, AvailabilityResponse,
    WhatsAppMessageSend
)

class N8NService:
    
    def __init__(self):
        self.base_url = settings.n8n_webhook_url
        self.api_key = settings.n8n_api_key
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def _make_request(
        self,
        endpoint: str,
        method: str = "POST",
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Faz uma requisição para o N8N"""
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "X-N8N-API-KEY": self.api_key
        }
        
        try:
            if method == "POST":
                response = await self.client.post(url, json=data, headers=headers)
            elif method == "GET":
                response = await self.client.get(url, headers=headers)
            else:
                raise ValueError(f"Método não suportado: {method}")
            
            response.raise_for_status()
            return response.json()
        
        except httpx.HTTPError as e:
            logger.error(f"Erro na requisição para N8N: {e}")
            raise
    
    async def check_availability(self, availability_check: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verifica disponibilidade de datas através do N8N
        
        Args:
            availability_check: Dados da verificação
            
        Returns:
            Resposta com disponibilidade
        """
        try:
            result = await self._make_request(
                "check-availability",
                method="POST",
                data=availability_check
            )
            return result
        except Exception as e:
            logger.error(f"Erro ao verificar disponibilidade: {e}")
            # Retorna resposta padrão em caso de erro
            return {
                "available": False,
                "message": "Não foi possível verificar a disponibilidade no momento. Por favor, tente novamente.",
                "spaces_available": [],
                "alternative_dates": []
            }
    
    async def create_booking(self, booking_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria uma nova reserva através do N8N
        
        Args:
            booking_data: Dados da reserva
            
        Returns:
            Resposta com dados da reserva criada
        """
        try:
            result = await self._make_request(
                "create-booking",
                method="POST",
                data=booking_data
            )
            return result
        except Exception as e:
            logger.error(f"Erro ao criar reserva: {e}")
            return {
                "success": False,
                "message": f"Erro ao criar reserva: {str(e)}",
                "booking_id": None
            }
    
    async def send_whatsapp_message(self, message_data: WhatsAppMessageSend) -> Dict[str, Any]:
        """
        Envia mensagem via WhatsApp através do N8N
        
        Args:
            message_data: Dados da mensagem
            
        Returns:
            Resposta do envio
        """
        try:
            result = await self._make_request(
                "send-whatsapp",
                method="POST",
                data=message_data.dict()
            )
            return result
        except Exception as e:
            logger.error(f"Erro ao enviar mensagem WhatsApp: {e}")
            return {
                "success": False,
                "message": f"Erro ao enviar mensagem: {str(e)}"
            }
    
    async def notify_new_booking(self, booking_data: Dict[str, Any]) -> None:
        """
        Notifica sobre nova reserva (envia para N8N processar)
        
        Args:
            booking_data: Dados da reserva
        """
        try:
            await self._make_request(
                "notify-new-booking",
                method="POST",
                data=booking_data
            )
            logger.info(f"Notificação de nova reserva enviada: {booking_data.get('booking_id')}")
        except Exception as e:
            logger.error(f"Erro ao notificar nova reserva: {e}")
    
    async def log_conversation(self, session_id: str, messages: list) -> None:
        """
        Registra conversa no N8N para análise/backup
        
        Args:
            session_id: ID da sessão
            messages: Lista de mensagens
        """
        try:
            await self._make_request(
                "log-conversation",
                method="POST",
                data={
                    "session_id": session_id,
                    "messages": messages,
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        except Exception as e:
            logger.error(f"Erro ao registrar conversa: {e}")
    
    async def trigger_custom_workflow(
        self,
        workflow_name: str,
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Dispara um workflow customizado no N8N
        
        Args:
            workflow_name: Nome do workflow
            data: Dados para o workflow
            
        Returns:
            Resposta do workflow
        """
        try:
            result = await self._make_request(
                f"workflow/{workflow_name}",
                method="POST",
                data=data
            )
            return result
        except Exception as e:
            logger.error(f"Erro ao disparar workflow {workflow_name}: {e}")
            return {
                "success": False,
                "message": f"Erro ao executar workflow: {str(e)}"
            }
    
    async def close(self):
        """Fecha o cliente HTTP"""
        await self.client.aclose()


# Singleton do serviço N8N
n8n_service = N8NService()
