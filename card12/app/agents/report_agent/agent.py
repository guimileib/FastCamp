from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
import httpx
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")
COMPANY_PHONE = os.getenv("WHATSAPP_PHONE_NUMBER")  

SYSTEM_PROMPT = """Você é um assistente que cria relatórios concisos de conversas de atendimento.

Crie um relatório estruturado contendo:
1. Resumo da conversa
2. Interesse do cliente (baixo/médio/alto)
3. Próximos passos sugeridos
4. Informações coletadas (data, nº convidados, tipo evento)
5. Status (novo lead, agendamento pendente, confirmado, desistiu)

Seja objetivo e profissional.
"""

model = LiteLlm(model_id="gpt-4o-mini")
agent = Agent(model=model, system_instructions=SYSTEM_PROMPT)


async def send_report_to_company(report: str) -> bool:  
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{N8N_WEBHOOK_URL}/webhook/send-report",
                json={
                    "phone": COMPANY_PHONE,
                    "message": report,
                    "timestamp": datetime.now().isoformat()
                }
            )
            return response.status_code == 200
    except Exception as e:
        print(f"Erro ao enviar relatório: {e}")
        return False


async def execute(payload: dict) -> dict:
    conversation_history = payload.get("conversation_history", [])
    customer_name = payload.get("customer_name", "Cliente")
    customer_phone = payload.get("customer_phone", "Não informado")
    trigger = payload.get("trigger", "manual")
    
    conversation_text = "\n".join([
        f"{msg.get('role', 'user')}: {msg.get('content', '')}"
        for msg in conversation_history
    ])
    
    user_prompt = f"""Analise esta conversa e crie um relatório:

CLIENTE: {customer_name} ({customer_phone})
MOTIVO: {trigger}

CONVERSA:
{conversation_text}

Gere o relatório estruturado."""
    
    response = await agent.generate_content(user_prompt)
    report_text = response.text if hasattr(response, 'text') else str(response)
    
    final_report = f"""RELATÓRIO DE ATENDIMENTO

👤 Cliente: {customer_name}
📱 Telefone: {customer_phone}
⏰ Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}
🔔 Motivo: {trigger}

{report_text}
"""
    sent = await send_report_to_company(final_report)
    
    return {
        "report": final_report,
        "agent": "report_agent",
        "report_sent": sent,
        "should_send_whatsapp": False  # para não enviar para o cliente
    }
