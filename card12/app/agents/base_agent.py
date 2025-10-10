from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid


class EventType(Enum):
    START = "start"
    MESSAGE = "message"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    ERROR = "error"
    COMPLETE = "complete"


@dataclass
class AgentEvent:
    event_type: EventType
    timestamp: datetime = field(default_factory=datetime.now)
    data: Dict[str, Any] = field(default_factory=dict)
    agent_name: str = ""


@dataclass
class Tool:
    name: str
    description: str
    parameters: Dict[str, Any]
    function: Callable


@dataclass
class AgentContext:
    session_id: str
    user_id: str
    user_name: str
    message: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, str]] = field(default_factory=list)


@dataclass
class AgentResponse:
    agent_name: str
    response: str
    confidence: float
    events: List[AgentEvent] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    tools_used: List[str] = field(default_factory=list)


class BaseAgent(ABC):
    """ 
    Estrutura:
    - name: Nome do agente
    - description: Descrição do propósito
    - system_prompt: Instruções do sistema
    - tools: Lista de ferramentas disponíveis
    - model: Modelo LLM (LiteLlm ou OpenAI)
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        system_prompt: str,
        model: Optional[Any] = None,
        tools: Optional[List[Tool]] = None
    ):
        self.name = name
        self.description = description
        self.system_prompt = system_prompt
        self.model = model
        self.tools = tools or []
        self.events: List[AgentEvent] = []
    
    def add_tool(self, tool: Tool):
        """Adiciona uma ferramenta ao agente"""
        self.tools.append(tool)
    
    def emit_event(self, event_type: EventType, data: Dict[str, Any]):
        """Emite um evento"""
        event = AgentEvent(
            event_type=event_type,
            agent_name=self.name,
            data=data
        )
        self.events.append(event)
        return event
    
    @abstractmethod
    async def execute(self, context: AgentContext) -> AgentResponse:
        pass
    
    async def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        context = AgentContext(
            session_id=payload.get("session_id", str(uuid.uuid4())),
            user_id=payload.get("user_id", payload.get("chat_id", "unknown")),
            user_name=payload.get("user_name", "Cliente"),
            message=payload.get("message", ""),
            metadata=payload.get("metadata", {}),
            history=payload.get("history", [])
        )
        
        self.emit_event(EventType.START, {
            "session_id": context.session_id,
            "user_id": context.user_id,
            "message": context.message
        })
        
        try:
            #executa o agente
            response = await self.execute(context)
            
            self.emit_event(EventType.COMPLETE, {
                "response": response.response,
                "confidence": response.confidence
            })
            
            return {
                "response": response.response,
                "agent": self.name,
                "confidence": response.confidence,
                "events": [
                    {
                        "type": e.event_type.value,
                        "timestamp": e.timestamp.isoformat(),
                        "data": e.data
                    }
                    for e in response.events
                ],
                "metadata": response.metadata,
                "tools_used": response.tools_used
            }
        
        except Exception as e:
            self.emit_event(EventType.ERROR, {
                "error": str(e),
                "session_id": context.session_id
            })
            
            return {
                "response": "Desculpe, ocorreu um erro ao processar sua mensagem.",
                "agent": self.name,
                "confidence": 0.0,
                "error": str(e),
                "metadata": {"error_type": type(e).__name__}
            }
    
    def get_tools_schema(self) -> List[Dict[str, Any]]:
        # retorna as toos pro LLM
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.parameters
            }
            for tool in self.tools
        ]
