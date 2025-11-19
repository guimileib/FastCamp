from agents.base_agent import BaseAgent

class TreatmentAgent(BaseAgent):
    """Agente focado em planos de tratamento e recomendações."""
    def analyze(self, transcription, diagnostic_info):
        prompt = f"""
        Você é um Agente Especialista em Terapêutica e Tratamentos.
        
        Informações do Diagnóstico:
        {diagnostic_info}

        Com base na transcrição original e no diagnóstico acima, sugira:
        1. Plano de Tratamento Recomendado (Medicamentos, Terapias).
        2. Exames Complementares necessários.
        3. Recomendações de Estilo de Vida ou Cuidados ao Paciente.

        Transcrição Original:
        {transcription}
        """
        return self.generate(prompt)
