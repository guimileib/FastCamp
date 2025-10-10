import json
from dotenv import load_dotenv
import os
import re

load_dotenv()


def classify_message(message: str) -> dict:
    """
    Classifica a mensagem usando regras simples
    Retorna qual agente deve processar
    """
    message_lower = message.lower()
    
    # Palavras-chave para agendamento
    booking_keywords = [
        "reservar", "reserva", "agendar", "agenda", "marcar",
        "disponível", "disponibilidade", "data", "dia",
        "quero reservar", "gostaria de agendar"
    ]
    
    # Palavras-chave para atendimento geral
    maria_keywords = [
        "oi", "olá", "ola", "bom dia", "boa tarde", "boa noite",
        "preço", "preco", "valor", "quanto custa",
        "capacidade", "pessoas", "convidados",
        "espaço", "espaco", "local", "onde fica",
        "serviço", "servico", "inclui", "buffet"
    ]
    
    # Verifica se tem data mencionada (dia/mes ou dd/mm)
    has_date = bool(re.search(r'\d{1,2}[/\-]\d{1,2}', message) or 
                    re.search(r'dia \d{1,2}', message_lower))
    
    # Verifica se tem número de convidados
    has_guest_count = bool(re.search(r'\d+\s*(pessoas|convidados|pessoas)', message_lower))
    
    # Decisão
    if has_date and has_guest_count:
        # Cliente deu informações completas → criar booking
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
        # Atendimento geral
        return {
            "agent": "maria_agent",
            "reasoning": "Atendimento geral ou saudação",
            "action": None,
            "confidence": 0.7
        }


async def execute(payload: dict) -> dict:
    """
    Orquestra o fluxo: classifica mensagem e chama agente apropriado
    Por enquanto usa apenas maria_agent (atendimento geral)
    """
    message = payload.get("message", "")
    user_name = payload.get("user_name", "Cliente")
    chat_id = payload.get("chat_id", "")
    phone = payload.get("phone", "")
    context = payload.get("context", {})
    
    # 1. Classifica a mensagem
    decision = classify_message(message)
    
    chosen_agent = decision.get("agent", "maria_agent")
    action = decision.get("action")
    
    print(f"🤖 Host Agent: Roteando para {chosen_agent} (confiança: {decision.get('confidence')})")
    print(f"   Motivo: {decision.get('reasoning')}")
    
    # 2. Por enquanto, sempre usa maria_agent
    # TODO: Implementar booking_agent e report_agent quando necessário
    
    # Gera resposta da Maria (sem LLM por enquanto, usa regras)
    from ..maria_agent.agent import execute as maria_execute
    
    result = await maria_execute(payload)
    
    # Adiciona info do orquestrador
    result["orchestrator"] = {
        "chosen_agent": chosen_agent,
        "reasoning": decision.get("reasoning"),
        "confidence": decision.get("confidence")
    }
    
    return result

