from agents.base_agent import BaseAgent
from .task_manager import DiagnosticTaskManager

class DiagnosticAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.task_manager = DiagnosticTaskManager()

    def analyze(self, transcription, triage_info):
        prompt = f"""
        Você é um Agente Especialista em Diagnóstico Clínico.
        
        Informações da Triagem:
        {triage_info}

        Analise a transcrição médica abaixo e extraia:
        1. Lista de Sintomas (Subjetivos e Objetivos).
        2. Histórico Médico Relevante (Doenças prévias, cirurgias).
        3. Hipóteses Diagnósticas (Liste as 3 mais prováveis).

        Transcrição:
        {transcription}
        """
        return self.generate(prompt)
