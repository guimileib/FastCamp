from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict
import uvicorn

class PayloadModel(BaseModel):
    origin: str = None
    destination: str = None
    start_date: str = None
    end_date: str = None
    budget: float = None
    
    class Config:
        extra = "allow"  # Permite campos adicionais

def create_app(agent):
    app = FastAPI(title="Travel Agent API")
    
    @app.get("/")
    async def health_check():
        return {"status": "online", "agent": "travel_agent"}
    
    @app.post("/run")
    async def run(payload: PayloadModel):
        try:
            # Converte para dict para compatibilidade
            payload_dict = payload.dict(exclude_unset=True)
            result = await agent.execute(payload_dict)
            return result
        except Exception as e:
            return {"error": str(e), "type": type(e).__name__}
    
    return app

# a função create_app(agent) generaliza a rota para todos os agentes