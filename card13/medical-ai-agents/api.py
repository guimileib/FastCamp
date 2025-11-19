from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents.triage_agent.agent import TriageAgent
from agents.diagnostic_agent.agent import DiagnosticAgent
from agents.treatment_agent.agent import TreatmentAgent
from coordinator import CoordinatorAgent
import uvicorn

app = FastAPI(
    title="Medical AI Agents API",
    description="API centralizada para acesso aos agentes médicos inteligentes (Triagem, Diagnóstico, Tratamento)",
    version="1.0.0"
)

# --- Modelos de Dados (Request Body) ---
class TriageRequest(BaseModel):
    transcription: str

class DiagnosticRequest(BaseModel):
    transcription: str
    triage_info: str

class TreatmentRequest(BaseModel):
    transcription: str
    diagnostic_info: str

class FullWorkflowRequest(BaseModel):
    transcription: str
    description: str = "Solicitação via API"

# --- Inicialização dos Agentes ---
# Instanciamos globalmente para reutilizar a configuração
triage_agent = TriageAgent()
diagnostic_agent = DiagnosticAgent()
treatment_agent = TreatmentAgent()
coordinator = CoordinatorAgent()

# --- Endpoints Individuais ---

@app.post("/agents/triage", tags=["Agentes Individuais"])
async def run_triage(request: TriageRequest):
    """Executa apenas o Agente de Triagem."""
    try:
        result = triage_agent.analyze(request.transcription)
        return {"status": "success", "agent": "triage", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agents/diagnostic", tags=["Agentes Individuais"])
async def run_diagnostic(request: DiagnosticRequest):
    """Executa apenas o Agente de Diagnóstico (requer info da triagem)."""
    try:
        result = diagnostic_agent.analyze(request.transcription, request.triage_info)
        return {"status": "success", "agent": "diagnostic", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agents/treatment", tags=["Agentes Individuais"])
async def run_treatment(request: TreatmentRequest):
    """Executa apenas o Agente de Tratamento (requer info do diagnóstico)."""
    try:
        result = treatment_agent.analyze(request.transcription, request.diagnostic_info)
        return {"status": "success", "agent": "treatment", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Endpoint Coordenado (Fluxo Completo) ---

@app.post("/workflow/full", tags=["Workflow Completo"])
async def run_full_workflow(request: FullWorkflowRequest):
    """Executa o fluxo completo: Triagem -> Diagnóstico -> Tratamento."""
    try:
        # O coordinator já retorna um dicionário estruturado
        results = coordinator.process_case(request.transcription, request.description)
        return {"status": "success", "workflow_results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "Medical AI Agents API is running", "docs_url": "/docs"}

if __name__ == "__main__":
    # Executa o servidor na porta 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
