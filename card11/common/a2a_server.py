from fastapi import FastAPI
import uvicorn
def create_app(agent):
    app = FastAPI()
    @app.post("/run")
    async def run(payload: dict):
        return await agent.execute(payload)
    return app

# a função create_app(agent) generaliza a rota para todos os agentes