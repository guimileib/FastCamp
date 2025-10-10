from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from typing import List

from app.models.agent import AppInfo, AppListResponse
from config.settings import settings

router = APIRouter()


@router.get("/")
async def root():
    return RedirectResponse(url="/dev-ui")


@router.get("/dev-ui", response_class=HTMLResponse)
async def dev_ui():
    html_content = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Party Space Agent - Developer UI</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
            }
            .container {
                background: white;
                border-radius: 10px;
                padding: 30px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            }
            h1 {
                color: #667eea;
                border-bottom: 3px solid #667eea;
                padding-bottom: 10px;
            }
            .info-card {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
                border-left: 4px solid #667eea;
            }
            .endpoint {
                background: #e9ecef;
                padding: 15px;
                margin: 10px 0;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
            }
            .method {
                display: inline-block;
                padding: 3px 8px;
                border-radius: 3px;
                font-weight: bold;
                margin-right: 10px;
            }
            .get { background: #28a745; color: white; }
            .post { background: #007bff; color: white; }
            .delete { background: #dc3545; color: white; }
            .websocket { background: #6f42c1; color: white; }
            a {
                color: #667eea;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎉 Party Space Agent - Developer UI</h1>
            
            <div class="info-card">
                <h2>Informações do Agente</h2>
                <p><strong>Nome:</strong> Party Space Agent</p>
                <p><strong>Descrição:</strong> Agente de atendimento para espaço de festa</p>
                <p><strong>Status:</strong> ✅ Ativo</p>
            </div>
            
            <div class="info-card">
                <h2>Links Úteis</h2>
                <p>📚 <a href="/docs" target="_blank">Documentação API (Swagger)</a></p>
                <p>📖 <a href="/redoc" target="_blank">Documentação API (ReDoc)</a></p>
                <p>📋 <a href="/list-apps">Lista de Aplicações</a></p>
            </div>
            
            <div class="info-card">
                <h2>Principais Endpoints</h2>
                
                <h3>Interação com Agente</h3>
                <div class="endpoint">
                    <span class="method post">POST</span> /run - Executar agente (sync)
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> /run_sse - Executar agente (streaming)
                </div>
                <div class="endpoint">
                    <span class="method websocket">WS</span> /run_live - Conexão live com agente
                </div>
                
                <h3>Sessões</h3>
                <div class="endpoint">
                    <span class="method get">GET</span> /apps/{app_name}/users/{user_id}/sessions
                </div>
                <div class="endpoint">
                    <span class="method post">POST</span> /apps/{app_name}/users/{user_id}/sessions
                </div>
                
                <h3>Debug & Trace</h3>
                <div class="endpoint">
                    <span class="method get">GET</span> /debug/trace/session/{session_id}
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@router.get("/list-apps", response_model=AppListResponse)
async def list_apps():
    apps = [
        AppInfo(
            app_name=settings.agent_name,
            description=settings.agent_description,
            version="1.0.0",
            status="active",
            capabilities=[
                "atendimento_whatsapp",
                "verificacao_disponibilidade",
                "criacao_reservas",
                "informacoes_espaco",
                "integracao_n8n"
            ],
            metadata={
                "whatsapp_number": settings.whatsapp_phone_number,
                "supported_languages": ["pt-BR"],
                "max_capacity": 200
            }
        )
    ]
    
    return AppListResponse(apps=apps, total=len(apps))
