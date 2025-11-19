from agents.triage_agent.agent import TriageAgent
from agents.diagnostic_agent.agent import DiagnosticAgent
from agents.treatment_agent.agent import TreatmentAgent
from .task_manager import HostTaskManager

class HostAgent:
    def __init__(self):
        self.task_manager = HostTaskManager()
        # Inicializa os sub-agentes
        self.triage = TriageAgent()
        self.diagnostic = DiagnosticAgent()
        self.treatment = TreatmentAgent()

    def process_case(self, transcription, description="Caso Médico"):
        print(f"\n>>> Iniciando Processamento Multi-Agente (Host) para: {description}...")
        
        # Passo 1
        print("1. [Agente de Triagem] Analisando urgência e especialidade...")
        triage_result = self.triage.analyze(transcription)
        
        # Passo 2
        print("2. [Agente de Diagnóstico] Identificando sintomas e hipóteses...")
        diagnostic_result = self.diagnostic.analyze(transcription, triage_result)
        
        # Passo 3
        print("3. [Agente de Tratamento] Gerando plano terapêutico...")
        treatment_result = self.treatment.analyze(transcription, diagnostic_result)
        
        return {
            "triage": triage_result,
            "diagnostic": diagnostic_result,
            "treatment": treatment_result
        }
