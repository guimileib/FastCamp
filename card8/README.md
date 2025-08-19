
# Quick start with ADK

## Criando ambiente virtual
```
python -m venv .venv
macOS/Linux: source .venv/bin/activate
Windows CMD: .venv\Scripts\activate.bat
Windows PowerShell: .venv\Scripts\Activate.ps1
```
## Estrutura das páginas
```
parent_folder/
    multi_tool_agent/
        __init__.py
        agent.py
        .env 
``` 
## Para rodar:
```
adk run multi_tool_agent
```
Se estiver usando Windows você precisará ativar o "Developer Mode" nas configurações do Windows. Pois, ele limita por padrão administradores, com modo desenvolvedor ativado conseguimos criar symlinks, sem ocorrer erros de privilégio.
