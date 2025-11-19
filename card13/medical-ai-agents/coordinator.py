from agents.triage_agent.agent import TriageAgent
from agents.diagnostic_agent.agent import DiagnosticAgent
from agents.treatment_agent.agent import TreatmentAgent

class CoordinatorAgent:
    """Gerencia o fluxo de trabalho entre os agentes."""
    def __init__(self):
        self.triage = TriageAgent()
        self.diagnostic = DiagnosticAgent()
        self.treatment = TreatmentAgent()

    def process_case(self, transcription, description="Caso Médico"):
        print(f"\n>>> Iniciando Processamento Multi-Agente para: {description}...")
        
        # Passo 1: Triagem
        print("1. [Agente de Triagem] Analisando urgência e especialidade...")
        triage_result = self.triage.analyze(transcription)
        
        # Passo 2: Diagnóstico
        print("2. [Agente de Diagnóstico] Identificando sintomas e hipóteses...")
        diagnostic_result = self.diagnostic.analyze(transcription, triage_result)
        
        # Passo 3: Tratamento
        print("3. [Agente de Tratamento] Gerando plano terapêutico...")
        treatment_result = self.treatment.analyze(transcription, diagnostic_result)
        
        return {
            "triage": triage_result,
            "diagnostic": diagnostic_result,
            "treatment": treatment_result
        }
