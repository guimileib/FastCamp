from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from sse_starlette.sse import EventSourceResponse
from typing import AsyncGenerator
import json
import uuid
import asyncio

from app.models.agent import AgentRunRequest, AgentRunResponse, AgentEvent, AgentEventType
from app.models.session import Message, MessageRole
from app.agents.party_agent import PartySpaceAgent
from app.services.session_service import session_service
from app.services.n8n_service import n8n_service

router = APIRouter()

party_agent = PartySpaceAgent(n8n_service)


@router.post("/run", response_model=AgentRunResponse)
async def run_agent(request: AgentRunRequest):
    session_id = request.session_id or str(uuid.uuid4())
    session = session_service.get_session(request.app_name, request.user_id, session_id)
    
    if not session:
        session = session_service.create_session(
            app_name=request.app_name,
            user_id=request.user_id,
            session_id=session_id,
            metadata=request.metadata
        )
    
    user_message = Message(
        role=MessageRole.USER,
        content=request.message,
        metadata=request.metadata
    )
    session_service.add_message(session_id, user_message)
    
    try:
        result = await party_agent.process_message(
            message=request.message,
            session_id=session_id,
            user_id=request.user_id,
            context=request.metadata
        )
        
        assistant_message = Message(
            role=MessageRole.ASSISTANT,
            content=result.get("response", ""),
            metadata=result.get("metadata", {})
        )
        session_service.add_message(session_id, assistant_message)
        
        events = [
            AgentEvent(
                event_type=AgentEventType.START,
                data={"session_id": session_id, "user_id": request.user_id}
            ),
            AgentEvent(
                event_type=AgentEventType.MESSAGE,
                data={"content": request.message, "role": "user"}
            ),
            AgentEvent(
                event_type=AgentEventType.MESSAGE,
                data={"content": result.get("response", ""), "role": "assistant"}
            ),
            AgentEvent(
                event_type=AgentEventType.COMPLETE,
                data={"status": "success"}
            )
        ]
        
        return AgentRunResponse(
            session_id=session_id,
            user_id=request.user_id,
            app_name=request.app_name,
            message=request.message,
            response=result.get("response", ""),
            events=events,
            metadata=result.get("metadata", {})
        )
        
    except Exception as e:
        error_event = AgentEvent(
            event_type=AgentEventType.ERROR,
            data={"error": str(e)}
        )
        
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar mensagem: {str(e)}"
        )


@router.post("/run_sse")
async def run_agent_sse(request: AgentRunRequest):
    async def event_generator() -> AsyncGenerator:
        session_id = request.session_id or str(uuid.uuid4())
        session = session_service.get_session(request.app_name, request.user_id, session_id)
        
        if not session:
            session = session_service.create_session(
                app_name=request.app_name,
                user_id=request.user_id,
                session_id=session_id,
                metadata=request.metadata
            )
        
        yield {
            "event": "start",
            "data": json.dumps({
                "session_id": session_id,
                "user_id": request.user_id
            })
        }
        
        user_message = Message(
            role=MessageRole.USER,
            content=request.message,
            metadata=request.metadata
        )
        session_service.add_message(session_id, user_message)
        
        yield {
            "event": "message",
            "data": json.dumps({
                "role": "user",
                "content": request.message
            })
        }
        
        try:
            yield {
                "event": "thinking",
                "data": json.dumps({"status": "processing"})
            }
            
            result = await party_agent.process_message(
                message=request.message,
                session_id=session_id,
                user_id=request.user_id,
                context=request.metadata
            )
            
            assistant_message = Message(
                role=MessageRole.ASSISTANT,
                content=result.get("response", ""),
                metadata=result.get("metadata", {})
            )
            session_service.add_message(session_id, assistant_message)
            
            yield {
                "event": "message",
                "data": json.dumps({
                    "role": "assistant",
                    "content": result.get("response", "")
                })
            }
            
            yield {
                "event": "complete",
                "data": json.dumps({
                    "status": "success",
                    "session_id": session_id
                })
            }
            
        except Exception as e:
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)})
            }
    
    return EventSourceResponse(event_generator())


@router.websocket("/run_live")
async def run_agent_live(websocket: WebSocket):
    await websocket.accept()
    
    session_id = None
    user_id = None
    app_name = None
    
    try:
        init_message = await websocket.receive_json()
        
        app_name = init_message.get("app_name")
        user_id = init_message.get("user_id")
        session_id = init_message.get("session_id") or str(uuid.uuid4())
        
        session = session_service.get_session(app_name, user_id, session_id)
        if not session:
            session = session_service.create_session(
                app_name=app_name,
                user_id=user_id,
                session_id=session_id
            )
        
        await websocket.send_json({
            "type": "connection_established",
            "session_id": session_id,
            "user_id": user_id
        })
        
        # Loop de mensagens
        while True:
            message_data = await websocket.receive_json()
            message_type = message_data.get("type", "text")
            content = message_data.get("content", "")
            
            if message_type == "ping":
                await websocket.send_json({"type": "pong"})
                continue
            
            if message_type == "close":
                break
            
            # Adiciona mensagem do usuário
            user_message = Message(
                role=MessageRole.USER,
                content=content,
                metadata={"type": message_type}
            )
            session_service.add_message(session_id, user_message)
            
            # Envia confirmação de recebimento
            await websocket.send_json({
                "type": "message_received",
                "content": content
            })
            
            # Processa com o agente
            try:
                result = await party_agent.process_message(
                    message=content,
                    session_id=session_id,
                    user_id=user_id,
                    context={"type": message_type}
                )
                
                # Adiciona resposta do agente
                assistant_message = Message(
                    role=MessageRole.ASSISTANT,
                    content=result.get("response", ""),
                    metadata=result.get("metadata", {})
                )
                session_service.add_message(session_id, assistant_message)
                
                # Envia resposta
                await websocket.send_json({
                    "type": "message",
                    "role": "assistant",
                    "content": result.get("response", ""),
                    "metadata": result.get("metadata", {})
                })
                
            except Exception as e:
                await websocket.send_json({
                    "type": "error",
                    "error": str(e)
                })
    
    except WebSocketDisconnect:
        print(f"WebSocket desconectado: session_id={session_id}")
    except Exception as e:
        print(f"Erro no WebSocket: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "error": str(e)
            })
        except:
            pass
    finally:
        try:
            await websocket.close()
        except:
            pass
