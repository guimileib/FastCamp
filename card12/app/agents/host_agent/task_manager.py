from .agent import execute

async def run(payload):
    """Executa o orquestrador host_agent"""
    return await execute(payload)