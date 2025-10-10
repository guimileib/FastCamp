import httpx
import os
from datetime import datetime
from dotenv import load_dotenv
from typing import Dict, Any
import re

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, AgentContext, AgentResponse, EventType, Tool

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

SYSTEM_PROMPT = """Você é um assistente especializado em agendamento de eventos do Espaço Vila do Sol.

Sua função é extrair e confirmar informações de reserva:

✅ INFORMAÇÕES NECESSÁRIAS:
1. Data do evento (dia/mês/ano)
2. Horário/período (manhã, tarde, noite, integral)
3. Quantidade de convidados
4. Tipo de evento (aniversário, casamento, formatura, etc)
5. Nome completo do cliente
6. Telefone de contato

📋 PROCESSO:
- Quando faltar informação, pergunte de forma natural
- Confirme todas as informações antes de criar o agendamento
- Seja claro sobre o que está incluso no espaço
- Informe que após confirmação, será enviado um contrato

💡 DICAS:
- Use emojis para deixar a conversa mais leve
- Seja profissional mas amigável
- Destaque os diferenciais do espaço

IMPORTANTE: Sempre confirme com o cliente antes de finalizar a reserva.
"""


class BookingAgent(BaseAgent):

    def __init__(self):
        super().__init__(
            name="booking_agent",
            description="Agente de agendamento e criação de reservas no Espaço Vila do Sol",
            system_prompt=SYSTEM_PROMPT,
            model=None
        )
        
        # tool de criação de booking-marcar
        self.add_tool(Tool(
            name="create_booking_supabase",
            description="Cria uma reserva no banco de dados Supabase",
            parameters={
                "customer_name": "str",
                "customer_phone": "str",
                "event_date": "str (YYYY-MM-DD)",
                "event_time": "str",
                "guest_count": "int",
                "event_type": "str",
                "notes": "str"
            },
            function=self.create_booking_tool
        ))
    
    async def create_booking_tool(self, booking_data: Dict[str, Any]) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SUPABASE_URL}/rest/v1/bookings",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation"
                },
                json=booking_data
            )
            
            if response.status_code in [200, 201]:
                return {"success": True, "booking": response.json()}
            else:
                return {"success": False, "error": response.text}
    
    def extract_booking_info(self, message: str, user_name: str, phone: str) -> Dict[str, Any]:
        date_match = re.search(r'(\d{1,2})[/\-](\d{1,2})(?:[/\-](\d{2,4}))?', message)
        event_date = None
        if date_match:
            day, month, year = date_match.groups()
            year = year or "2025"
            if len(year) == 2:
                year = "20" + year
            event_date = f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        
        guest_match = re.search(r'(\d+)\s*(pessoas|convidados|pessoas)', message.lower())
        guest_count = int(guest_match.group(1)) if guest_match else None

        message_lower = message.lower()
        event_time = "18:00"  
        if "manhã" in message_lower or "manha" in message_lower:
            event_time = "09:00"
        elif "tarde" in message_lower:
            event_time = "14:00"
        elif "noite" in message_lower:
            event_time = "19:00"
        
        event_type = "festa"
        if "aniversário" in message_lower or "aniversario" in message_lower:
            event_type = "aniversário"
        elif "casamento" in message_lower:
            event_type = "casamento"
        elif "formatura" in message_lower:
            event_type = "formatura"
        elif "infantil" in message_lower:
            event_type = "festa infantil"
        
        return {
            "event_date": event_date,
            "event_time": event_time,
            "guest_count": guest_count,
            "event_type": event_type,
            "customer_name": user_name,
            "customer_phone": phone
        }
    
    async def execute(self, context: AgentContext) -> AgentResponse:

        print(f"Booking Agent: Processando mensagem de {context.user_name}")
        print(f"   Mensagem: {context.message}")
        
        self.emit_event(EventType.MESSAGE, {
            "user": context.user_name,
            "message": context.message
        })
        
        try:
            action = context.metadata.get("action", "check_info")
            
            booking_info = self.extract_booking_info(
                context.message,
                context.user_name,
                context.metadata.get("phone", "")
            )
            
            print(f"   📋 Informações extraídas: {booking_info}")
            
            missing_info = []
            if not booking_info["event_date"]:
                missing_info.append("data do evento")
            if not booking_info["guest_count"]:
                missing_info.append("quantidade de convidados")
            
            if missing_info and action != "create_booking":
                response_text = f"Ok! Para confirmar sua reserva, preciso de mais alguns detalhes:\n\n"
                response_text += "? " + "\n? ".join(missing_info)
                response_text += "\n\nPode me passar essas informações? 😊"
                
                return AgentResponse(
                    agent_name=self.name,
                    response=response_text,
                    confidence=0.7,
                    events=self.events.copy(),
                    metadata={"missing_info": missing_info, "booking_info": booking_info},
                    tools_used=[]
                )
            
            # se tiver tudo vai criar o booking
            booking_data = {
                "customer_name": booking_info["customer_name"],
                "customer_phone": booking_info["customer_phone"],
                "chat_id": context.user_id,
                "event_date": booking_info["event_date"],
                "event_time": booking_info["event_time"],
                "guest_count": booking_info["guest_count"],
                "event_type": booking_info["event_type"],
                "status": "pending",
                "created_at": datetime.now().isoformat(),
                "notes": context.message
            }
            
            self.emit_event(EventType.TOOL_CALL, {
                "tool": "create_booking_supabase",
                "data": booking_data
            })
            
            result = await self.create_booking_tool(booking_data)
            
            self.emit_event(EventType.TOOL_RESULT, {
                "tool": "create_booking_supabase",
                "success": result["success"]
            })
            
            if result["success"]:
                booking_id = result["booking"][0]["id"]
                response_text = f"""✅ Reserva criada com sucesso!

📋 Número da reserva: #{booking_id}
📅 Data: {booking_info['event_date']}
⏰ Horário: {booking_info['event_time']}
👥 Convidados: {booking_info['guest_count']} pessoas
🎉 Tipo: {booking_info['event_type']}

Em breve entrarei em contato para confirmar os detalhes e enviar o contrato! 📄✨"""
                
                return AgentResponse(
                    agent_name=self.name,
                    response=response_text,
                    confidence=0.95,
                    events=self.events.copy(),
                    metadata={"booking_created": True, "booking_id": booking_id, "booking_data": result["booking"][0]},
                    tools_used=["create_booking_supabase"]
                )
            else:
                return AgentResponse(
                    agent_name=self.name,
                    response="Ops! Tive um problema ao criar a reserva. Pode tentar novamente em alguns instantes?",
                    confidence=0.3,
                    events=self.events.copy(),
                    metadata={"booking_created": False, "error": result["error"]},
                    tools_used=["create_booking_supabase"]
                )
        
        except Exception as e:
            print(f"Erro no Booking Agent: {e}")
            import traceback
            traceback.print_exc()
            
            # Emite evento de erro
            self.emit_event(EventType.ERROR, {
                "error": str(e),
                "error_type": type(e).__name__
            })
            
            return AgentResponse(
                agent_name=self.name,
                response="Desculpe, tive um problema ao processar sua reserva. Tente novamente em alguns instantes! 😅",
                confidence=0.0,
                events=self.events.copy(),
                metadata={"error": str(e)},
                tools_used=[]
            )


booking_agent = BookingAgent()


async def execute(payload: dict) -> dict:
    result = await booking_agent.run(payload)
    return result
