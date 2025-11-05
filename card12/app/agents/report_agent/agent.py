import httpx
import os
from datetime import datetime
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")
COMPANY_PHONE = os.getenv("WHATSAPP_PHONE_NUMBER")

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

SYSTEM_PROMPT = """Você é um assistente que cria relatórios concisos de conversas de atendimento.

Crie um relatório estruturado contendo:
1. Resumo da conversa
2. Interesse do cliente (baixo/médio/alto)
3. Próximos passos sugeridos
4. Informações coletadas (data, nº convidados, tipo evento)
5. Status (novo lead, agendamento pendente, confirmado, desistiu)

Seja objetivo e profissional.
"""


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
    lead_analysis = payload.get("lead_analysis", {})
    
    conversation_text = "\n".join([
        f"{msg.get('role', 'user')}: {msg.get('content', '')}"
        for msg in conversation_history
    ])
    
    # Se for lead quente, adiciona contexto ao prompt
    lead_context = ""
    if "Lead Quente" in trigger:
        lead_context = f"""
⚠️ ATENÇÃO: LEAD QUENTE DETECTADO! ⚠️

🌡️ Temperatura: {lead_analysis.get('temperature', 'N/A')}
📊 Score: {lead_analysis.get('hot_score', 0)}/8
🎯 Prioridade: {lead_analysis.get('priority', 'N/A')}

Indicadores detectados:
- Data específica: {lead_analysis.get('indicators', {}).get('specific_date', False)}
- Número de convidados: {lead_analysis.get('indicators', {}).get('guest_count', False)}
- Consulta de preço: {lead_analysis.get('indicators', {}).get('price_inquiry', False)}
- Urgência: {any(word in conversation_text.lower() for word in lead_analysis.get('indicators', {}).get('urgency', []))}
- Comprometimento: {any(word in conversation_text.lower() for word in lead_analysis.get('indicators', {}).get('commitment', []))}

⏰ AÇÃO RECOMENDADA: Entrar em contato IMEDIATAMENTE (telefone/WhatsApp)
"""
    
    user_prompt = f"""Analise esta conversa e crie um relatório:

👤 CLIENTE: {customer_name}
📱 TELEFONE: {customer_phone}
🔔 MOTIVO: {trigger}

{lead_context}

📝 CONVERSA:
{conversation_text}

Gere um relatório estruturado com:
1. Resumo da conversa
2. Nível de interesse (baixo/médio/alto/URGENTE)
3. Informações coletadas (data, nº convidados, tipo evento)
4. Próximos passos sugeridos
5. Observações importantes"""
    
    # Usa OpenAI para gerar o relatório
    response = await openai_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
        max_tokens=800
    )
    
    report_text = response.choices[0].message.content.strip()
    
    # Emoji de prioridade baseado no lead
    priority_emoji = "🔥" if "Lead Quente" in trigger else "📊"
    
    final_report = f"""{priority_emoji} RELATÓRIO DE ATENDIMENTO {priority_emoji}

👤 Cliente: {customer_name}
📱 Telefone: {customer_phone}
⏰ Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M')}
🔔 Motivo: {trigger}

{report_text}

{'='*50}
💡 DICA: Responda o cliente dentro de 5 minutos para aumentar as chances de fechamento!
"""
    
    sent = await send_report_to_company(final_report)
    
    return {
        "report": final_report,
        "agent": "report_agent",
        "report_sent": sent,
        "should_send_whatsapp": False,  # para não enviar para o cliente
        "lead_temperature": lead_analysis.get('temperature', 'N/A')
    }
