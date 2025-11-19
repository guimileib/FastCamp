class HostTaskManager:
    """
    Gerencia o fluxo de tarefas do Host Agent.
    Pode ser expandido para salvar estado, logs ou gerenciar erros.
    """
    def get_workflow_steps(self):
        return [
            "Triagem",
            "Diagnóstico",
            "Tratamento"
        ]
