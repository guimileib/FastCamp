from fastapi import APIRouter, HTTPException, Path, Body
from typing import Optional
import uuid

from app.models.session import SessionCreate, SessionResponse, SessionList
from app.services.session_service import session_service

router = APIRouter()


@router.get(
    "/apps/{app_name}/users/{user_id}/sessions/{session_id}",
    response_model=SessionResponse
)
async def get_session(
    app_name: str = Path(..., description="Nome da aplicação"),
    user_id: str = Path(..., description="ID do usuário"),
    session_id: str = Path(..., description="ID da sessão")
):
    session = session_service.get_session(app_name, user_id, session_id)
    
    if not session:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    
    return SessionResponse(
        session_id=session.session_id,
        user_id=session.user_id,
        app_name=session.app_name,
        message_count=len(session.messages),
        created_at=session.created_at,
        updated_at=session.updated_at,
        metadata=session.metadata
    )


@router.get(
    "/apps/{app_name}/users/{user_id}/sessions",
    response_model=SessionList
)
async def list_sessions(
    app_name: str = Path(..., description="Nome da aplicação"),
    user_id: str = Path(..., description="ID do usuário"),
    exclude_eval: bool = True
):
    sessions = session_service.list_sessions(app_name, user_id, exclude_eval)
    
    return SessionList(
        sessions=sessions,
        total=len(sessions)
    )


@router.post(
    "/apps/{app_name}/users/{user_id}/sessions/{session_id}",
    response_model=SessionResponse,
    status_code=201
)
async def create_session_with_id(
    app_name: str = Path(..., description="Nome da aplicação"),
    user_id: str = Path(..., description="ID do usuário"),
    session_id: str = Path(..., description="ID da sessão"),
    session_data: SessionCreate = Body(...)
):
    session = session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        metadata=session_data.metadata
    )
    
    return SessionResponse(
        session_id=session.session_id,
        user_id=session.user_id,
        app_name=session.app_name,
        message_count=len(session.messages),
        created_at=session.created_at,
        updated_at=session.updated_at,
        metadata=session.metadata
    )


@router.post(
    "/apps/{app_name}/users/{user_id}/sessions",
    response_model=SessionResponse,
    status_code=201
)
async def create_session(
    app_name: str = Path(..., description="Nome da aplicação"),
    user_id: str = Path(..., description="ID do usuário"),
    session_data: SessionCreate = Body(...)
):
    session_id = session_data.session_id or str(uuid.uuid4())
    
    session = session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
        metadata=session_data.metadata
    )
    
    return SessionResponse(
        session_id=session.session_id,
        user_id=session.user_id,
        app_name=session.app_name,
        message_count=len(session.messages),
        created_at=session.created_at,
        updated_at=session.updated_at,
        metadata=session.metadata
    )


@router.delete(
    "/apps/{app_name}/users/{user_id}/sessions/{session_id}",
    status_code=204
)
async def delete_session(
    app_name: str = Path(..., description="Nome da aplicação"),
    user_id: str = Path(..., description="ID do usuário"),
    session_id: str = Path(..., description="ID da sessão")
):
    success = session_service.delete_session(app_name, user_id, session_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    
    return None
