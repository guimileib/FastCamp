import json
from dotenv import load_dotenv
import os
import re
from openai import AsyncOpenAI

load_dotenv()

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

CLASSIFICATION_PROMPT = """Você é um assistente especializado em classificar mensagens de clientes para rotear para o agente correto.

AGENTES DISPONÍVEIS:
1. **maria_agent** - Atendimento geral, informações sobre o espaço, preços, capacidade
2. **booking_agent** - Criação de reservas quando o cliente já forneceu data e número de convidados

INSTRUÇÕES:
- Analise a mensagem do cliente
- Identifique a intenção principal
- Retorne APENAS o nome do agente: "maria_agent" ou "booking_agent"

REGRAS:
- Se o cliente menciona DATA ESPECÍFICA + NÚMERO DE CONVIDADOS → booking_agent
- Se o cliente quer "reservar", "agendar" mas NÃO deu informações completas → maria_agent
- Saudações, perguntas sobre preço, capacidade, localização → maria_agent
- Qualquer dúvida ou pergunta geral → maria_agent

Responda APENAS com o nome do agente, sem explicações.
"""


async def classify_message_with_llm(message: str, user_name: str = "Cliente") -> dict:
    """Classifica mensagem usando LLM para decisão mais inteligente"""
    try:
        response = await openai_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": CLASSIFICATION_PROMPT},
                {"role": "user", "content": f"Cliente: {user_name}\nMensagem: {message}"}
            ],
            temperature=0.3,
            max_tokens=50
        )
        
        agent_choice = response.choices[0].message.content.strip().lower()
        
        # Validação
        if "booking" in agent_choice:
            chosen_agent = "booking_agent"
            confidence = 0.9
            reasoning = "Cliente forneceu informações completas para reserva"
        else:
            chosen_agent = "maria_agent"
            confidence = 0.85
            reasoning = "Atendimento geral ou coleta de informações"
        
        print(f"🤖 LLM Classification: {chosen_agent} (confiança: {confidence})")
        
        return {
            "agent": chosen_agent,
            "reasoning": reasoning,
            "confidence": confidence
        }
    
    except Exception as e:
        print(f"⚠️ Erro na classificação LLM: {e}")
        # Fallback para classificação baseada em regras
        return classify_message_fallback(message)


def classify_message_fallback(message: str) -> dict:
    """Classificação de fallback usando regras (backup se LLM falhar)"""
    message_lower = message.lower()
    
    # palavras-chave para agendamento
    booking_keywords = [
        "reservar", "reserva", "agendar", "agenda", "marcar",
        "disponível", "disponibilidade", "data", "dia",
        "quero reservar", "gostaria de agendar"
    ]
    
    # palavras-chave para atendimento geral
    maria_keywords = [
        "oi", "olá", "ola", "bom dia", "boa tarde", "boa noite",
        "preço", "preco", "valor", "quanto custa",
        "capacidade", "pessoas", "convidados",
        "espaço", "espaco", "local", "onde fica",
        "serviço", "servico", "inclui", "buffet"
    ]
    
    # verifica se tem data mencionada (dia/mes ou dd/mm)
    has_date = bool(re.search(r'\d{1,2}[/\-]\d{1,2}', message) or 
                    re.search(r'dia \d{1,2}', message_lower))
    
    #verificacao numero de convidados
    has_guest_count = bool(re.search(r'\d+\s*(pessoas|convidados|pessoas)', message_lower))

    if has_date and has_guest_count:
        # cliente deu informações completas → criar booking
        return {
            "agent": "booking_agent",
            "reasoning": "Cliente forneceu data e número de convidados",
            "action": "create_booking",
            "confidence": 0.9
        }
    
    elif any(keyword in message_lower for keyword in booking_keywords):
        # Interesse em agendar
        return {
            "agent": "booking_agent",
            "reasoning": "Cliente demonstrou interesse em agendar",
            "action": "check_info",
            "confidence": 0.8
        }
    
    else:
        return {
            "agent": "maria_agent",
            "reasoning": "Atendimento geral ou saudação",
            "action": None,
            "confidence": 0.7
        }


def analyze_lead_temperature(message: str, conversation_history: list = None) -> dict:
    """Analisa se o lead está quente (pronto para fechar) baseado na conversa"""
    message_lower = message.lower()
    
    hot_indicators = {
        "urgency": ["urgente", "rápido", "preciso logo", "hoje", "amanhã", "essa semana"],
        "commitment": ["quero reservar", "vou reservar", "quero agendar", "vou agendar", "pode marcar"],
        "specific_date": bool(re.search(r'\d{1,2}[/\-]\d{1,2}', message)),
        "guest_count": bool(re.search(r'\d+\s*(pessoas|convidados)', message_lower)),
        "price_inquiry": any(word in message_lower for word in ["preço", "preco", "valor", "quanto custa", "orçamento"]),
        "availability": any(word in message_lower for word in ["disponível", "disponibilidade", "tem vaga", "está livre"])
    }
    
    # Contagem de indicadores quentes
    hot_score = sum([
        1 if any(word in message_lower for word in hot_indicators["urgency"]) else 0,
        2 if any(word in message_lower for word in hot_indicators["commitment"]) else 0,
        2 if hot_indicators["specific_date"] else 0,
        2 if hot_indicators["guest_count"] else 0,
        1 if hot_indicators["price_inquiry"] else 0,
        1 if hot_indicators["availability"] else 0
    ])
    
    # Classificação
    if hot_score >= 4:
        temperature = "🔥 QUENTE"
        priority = "ALTA"
        should_notify = True
    elif hot_score >= 2:
        temperature = "🌡️ MORNO"
        priority = "MÉDIA"
        should_notify = False
    else:
        temperature = "❄️ FRIO"
        priority = "BAIXA"
        should_notify = False
    
    return {
        "temperature": temperature,
        "priority": priority,
        "hot_score": hot_score,
        "should_notify_company": should_notify,
        "indicators": hot_indicators
    }


async def execute(payload: dict) -> dict:
    message = payload.get("message", "")
    user_name = payload.get("user_name", "Cliente")
    chat_id = payload.get("chat_id", "")
    phone = payload.get("phone", "")
    context = payload.get("context", {})
    conversation_history = payload.get("conversation_history", [])
    
    # 1️⃣ Classifica a mensagem usando LLM
    decision = await classify_message_with_llm(message, user_name)
    
    chosen_agent = decision.get("agent", "maria_agent")
    action = decision.get("action")
    
    print(f"🤖 Host Agent: Roteando para {chosen_agent} (confiança: {decision.get('confidence')})")
    print(f"   Motivo: {decision.get('reasoning')}")
    
    # 2️⃣ Analisa temperatura do lead
    lead_analysis = analyze_lead_temperature(message, conversation_history)
    print(f"🌡️ Lead Temperature: {lead_analysis['temperature']} (score: {lead_analysis['hot_score']})")
    
    # 3️⃣ Roteia para o agente correto
    if chosen_agent == "booking_agent":
        from ..booking_agent.agent import execute as booking_execute
        result = await booking_execute(payload)
    else:
        from ..maria_agent.agent import execute as maria_execute
        result = await maria_execute(payload)
    
    # 4️⃣ Se lead está quente, notifica a empresa via Report Agent
    if lead_analysis["should_notify_company"]:
        print(f"🔥 LEAD QUENTE DETECTADO! Disparando Report Agent...")
        
        from ..report_agent.agent import execute as report_execute
        
        report_payload = {
            "conversation_history": conversation_history + [
                {"role": "user", "content": message},
                {"role": "assistant", "content": result.get("message", "")}
            ],
            "customer_name": user_name,
            "customer_phone": phone or chat_id,
            "trigger": f"Lead Quente - {lead_analysis['temperature']}",
            "lead_analysis": lead_analysis
        }
        
        try:
            report_result = await report_execute(report_payload)
            result["report_sent"] = report_result.get("report_sent", False)
            print(f"   ✅ Relatório enviado: {result['report_sent']}")
        except Exception as e:
            print(f"   ⚠️ Erro ao enviar relatório: {e}")
            result["report_sent"] = False
    
    # 5️⃣ Adiciona metadata do orquestrador
    result["orchestrator"] = {
        "chosen_agent": chosen_agent,
        "reasoning": decision.get("reasoning"),
        "confidence": decision.get("confidence"),
        "lead_analysis": lead_analysis
    }
    
    return result

