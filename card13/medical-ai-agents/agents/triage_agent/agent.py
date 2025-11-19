from agents.base_agent import BaseAgent
from .task_manager import TriageTaskManager

class TriageAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.task_manager = TriageTaskManager()

    def analyze(self, transcription):
        prompt = f"""
        Você é um Agente de Triagem Médica Sênior.
        Sua tarefa é analisar a transcrição abaixo e determinar:
        1. A Especialidade Médica mais provável (ex: Cardiologia, Neurologia).
        2. O Nível de Urgência (Baixo, Médio, Alto, Crítico) com uma breve justificativa.
        3. Um resumo de 1 frase do motivo da consulta.

        Transcrição:
        {transcription}
        
        Responda estritamente no formato:
        Especialidade: [Sua resposta]
        Urgência: [Sua resposta] - [Justificativa]
        Resumo: [Sua resposta]
        """
        return self.generate(prompt)
