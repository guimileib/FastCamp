"""
Rotas de debug e trace
"""

from fastapi import APIRouter, HTTPException, Path
from typing import List, Dict, Any
import uuid
from datetime import datetime

from app.models.trace import TraceResponse, TraceSpan

router = APIRouter()

traces_storage: Dict[str, List[TraceSpan]] = {}


@router.get("/debug/trace/{event_id}", response_model=TraceResponse)
async def get_trace_by_event(event_id: str = Path(..., description="ID do evento")):
    spans = traces_storage.get(event_id, [])
    
    if not spans:
        spans = [
            TraceSpan(
                span_id=str(uuid.uuid4()),
                event_id=event_id,
                session_id="session_example",
                operation_name="agent_execution",
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow(),
                duration_ms=150.5,
                status="success",
                tags={"event_type": "message", "user_id": "user_123"},
                logs=[
                    {"timestamp": datetime.utcnow().isoformat(), "message": "Iniciando processamento"},
                    {"timestamp": datetime.utcnow().isoformat(), "message": "Processamento concluído"}
                ]
            )
        ]
    
    return TraceResponse(
        event_id=event_id,
        session_id=spans[0].session_id if spans else "unknown",
        spans=spans,
        metadata={"total_spans": len(spans)}
    )


@router.get("/debug/trace/session/{session_id}", response_model=TraceResponse)
async def get_trace_by_session(session_id: str = Path(..., description="ID da sessão")):
    session_spans = []
    for event_id, spans in traces_storage.items():
        session_spans.extend([s for s in spans if s.session_id == session_id])
    
    if not session_spans:
        session_spans = [
            TraceSpan(
                span_id=str(uuid.uuid4()),
                event_id=f"event_{i}",
                session_id=session_id,
                operation_name=f"operation_{i}",
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow(),
                duration_ms=100.0 + i * 50,
                status="success",
                tags={"index": i},
                logs=[]
            )
            for i in range(3)
        ]
    
    return TraceResponse(
        event_id="session_trace",
        session_id=session_id,
        spans=session_spans,
        metadata={
            "total_spans": len(session_spans),
            "session_id": session_id
        }
    )
