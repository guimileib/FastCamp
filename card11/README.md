# Flight Agent - ADK e A2A


## Construção o sistema multiagente com ADK e A2A
- host_agent: Orquestra todos os outros agentes
- flight_agent: Encontra voos adequados
- stay_agent: Sugere acomodações
- activities_agent: Recomenda o envolvimento em atividades locais

ADK_demo/
├── agents/
│   ├── host_agent/
│   │   ├── agent.py              
│   │   ├── task_manager.py      
│   │   ├── __main__.py         
│   │   └── .well-known/
│   │       └── agent.json   
│   │
│   ├── flight_agent/
│   │   ├── agent.py        
│   │   ├── task_manager.py    
│   │   ├── __main__.py         
│   │   └── .well-known/
│   │       └── agent.json        
│   │
│   ├── stay_agent/
│   │   ├── agent.py              
│   │   ├── task_manager.py       
│   │   ├── __main__.py           
│   │   └── .well-known/
│   │       └── agent.json     
│   │
│   └── activities_agent/
│       ├── agent.py              
│       ├── task_manager.py       
│       ├── __main__.py           
│       └── .well-known/
│           └── agent.json       
│
├── common/
│   ├── a2a_client.py             # Utility to send requests to other agents
│   └── a2a_server.py             # Shared FastAPI A2A-compatible server template
│
├── shared/
│   └── schemas.py                # Shared Pydantic schema
│
├── streamlit_app.py             # Frontend UI for user input and response rendering
├── requirements.txt           
└── README.md           


## Rode o código
Start-Process uvicorn "agents.host_agent.__main__:app --port 8000"
Start-Process uvicorn "agents.flight_agent.__main__:app --port 8001"
Start-Process uvicorn "agents.stay_agent.__main__:app --port 8002"
Start-Process uvicorn "agents.activities_agent.__main__:app --port 8003"
streamlit run travel_ui.py

uvicorn agents.host_agent.__main__:app --port 8000
uvicorn agents.flight_agent.__main__:app --port 8001
uvicorn agents.stay_agent.__main__:app --port 8002
uvicorn agents.activities_agent.__main__:app --port 8003