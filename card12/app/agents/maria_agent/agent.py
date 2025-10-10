import os
from dotenv import load_dotenv
from openai import AsyncOpenAI
from typing import Dict, Any

import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent, AgentContext, AgentResponse, EventType, Tool

load_dotenv()

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

MARIA_PERSONALITY = """Você é Maria, assistente virtual do Espaço de Festas Vila do Sol! 🎉

PERSONALIDADE:
- Calorosa, amigável e acolhedora
- Usa emojis naturalmente (😊🎉✨💰📅)
- Faz perguntas para entender melhor as necessidades
- É proativa em oferecer informações relevantes

INFORMAÇÕES DO ESPAÇO:
📍 Localização: Divinópolis Minas Gerais, Rua Nova Lima 280, Bairro Bom Pastor
👥 Capacidade: 150 pessoas


✅ INCLUSO NO ALUGUEL:
- Mesas e cadeiras 
- Toalhas de mesa brancas
- Sistema de som 
- Iluminação ambiente
- Área kids com brinquedos
- Área de Jogos

DIRETRIZES:
1. Faça perguntas para qualificar o lead (tipo de evento, data, nº convidados)
2. Ofereça visita ao espaço quando apropriado
3. Se cliente perguntar sobre disponibilidade, informe que precisa verificar
4. Seja sempre positiva e motivadora

IMPORTANTE: Seja natural, conversacional e personalizada. Evite respostas genéricas ou robotizadas.
"""


class MariaAgent(BaseAgent):    
    def __init__(self):
        super().__init__(
            name="maria_agent",
            description="Agente de atendimento do Espaço Vila do Sol - qualificação de leads e informações gerais",
            system_prompt=MARIA_PERSONALITY,
            model=None  # Usamos OpenAI diretamente
        )
    
    async def execute(self, context: AgentContext) -> AgentResponse:
        print(f"Maria Agent: Processando mensagem de {context.user_name}")
        print(f"   Mensagem: {context.message}")
        
        self.emit_event(EventType.MESSAGE, {
            "user": context.user_name,
            "message": context.message
        })
        
        try:
            # mensagens para OpenAI
            messages = [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": f"[Cliente: {context.user_name}]\n\n{context.message}"}
            ]
            
            # add histórico 
            if context.history:
                messages = [messages[0]] + context.history[-4:] + [messages[1]]
            
            print(f"   🔄 Chamando OpenAI ({MODEL})...")
            
            response = await openai_client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=0.8,
                max_tokens=500,
                presence_penalty=0.6,
                frequency_penalty=0.3
            )

            ai_response = response.choices[0].message.content.strip()
            
            print(f"   ✅ Resposta OpenAI: {ai_response[:100]}...")
            
            self.emit_event(EventType.COMPLETE, {
                "response_length": len(ai_response),
                "tokens": response.usage.total_tokens if hasattr(response, 'usage') else None
            })
            
            return AgentResponse(
                agent_name=self.name,
                response=ai_response,
                confidence=0.85,
                events=self.events.copy(),
                metadata={
                    "model_used": MODEL,
                    "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None,
                    "user_name": context.user_name
                },
                tools_used=[]
            )
        
        except Exception as e:
            print(f"Erro ao chamar OpenAI: {e}")
            import traceback
            traceback.print_exc()
            
            self.emit_event(EventType.ERROR, {
                "error": str(e),
                "error_type": type(e).__name__
            })
            
            return AgentResponse(
                agent_name=self.name,
                response=f"Oi {context.user_name}! Desculpa, estou com uma dificuldade técnica agora. Pode tentar de novo? 😅",
                confidence=0.0,
                events=self.events.copy(),
                metadata={"error": str(e)},
                tools_used=[]
            )

maria_agent = MariaAgent()

async def execute(payload: dict) -> dict:
    result = await maria_agent.run(payload)
    return result
