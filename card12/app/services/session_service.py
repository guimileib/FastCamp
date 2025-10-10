from typing import Dict, List, Optional
from datetime import datetime
import uuid
from loguru import logger

from app.models.session import Session, SessionCreate, SessionResponse, Message


class SessionService: 
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
    
    def create_session(
        self,
        app_name: str,
        user_id: str,
        session_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Session:
        """Cria uma nova sessão"""
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        if session_id in self.sessions:
            logger.warning(f"Sessão {session_id} já existe. Retornando existente.")
            return self.sessions[session_id]
        
        session = Session(
            session_id=session_id,
            user_id=user_id,
            app_name=app_name,
            messages=[],
            metadata=metadata or {}
        )
        
        self.sessions[session_id] = session
        logger.info(f"Sessão criada: {session_id} para usuário {user_id}")
        return session
    
    def get_session(
        self,
        app_name: str,
        user_id: str,
        session_id: str
    ) -> Optional[Session]:
        session = self.sessions.get(session_id)
        
        if session and session.app_name == app_name and session.user_id == user_id:
            return session
        
        return None
    
    def list_sessions(
        self,
        app_name: str,
        user_id: str,
        exclude_eval: bool = True
    ) -> List[SessionResponse]:
        user_sessions = [
            session for session in self.sessions.values()
            if session.app_name == app_name 
            and session.user_id == user_id
            and (not exclude_eval or not session.is_eval_session)
        ]
        
        return [
            SessionResponse(
                session_id=s.session_id,
                user_id=s.user_id,
                app_name=s.app_name,
                message_count=len(s.messages),
                created_at=s.created_at,
                updated_at=s.updated_at,
                metadata=s.metadata
            )
            for s in user_sessions
        ]
    
    def delete_session(
        self,
        app_name: str,
        user_id: str,
        session_id: str
    ) -> bool:
        session = self.get_session(app_name, user_id, session_id)
        
        if session:
            del self.sessions[session_id]
            logger.info(f"Sessão deletada: {session_id}")
            return True
        
        return False
    
    def add_message(
        self,
        session_id: str,
        message: Message
    ) -> bool:
        session = self.sessions.get(session_id)
        
        if session:
            session.messages.append(message)
            session.updated_at = datetime.utcnow()
            logger.debug(f"Mensagem adicionada à sessão {session_id}")
            return True
        
        return False
    
    def get_session_messages(self, session_id: str) -> List[Message]:
        session = self.sessions.get(session_id)
        return session.messages if session else []
    
    def clear_session_messages(self, session_id: str) -> bool:
        session = self.sessions.get(session_id)
        
        if session:
            session.messages = []
            session.updated_at = datetime.utcnow()
            logger.info(f"Mensagens da sessão {session_id} limpas")
            return True
        
        return False

session_service = SessionService()
