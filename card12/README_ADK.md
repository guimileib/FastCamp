# 🎉 Party Agent API - Google ADK

API de agentes inteligentes para atendimento automatizado de Espaço de Festas, seguindo o padrão **Google ADK (Agent Development Kit)**.

## 🌟 Características

- ✅ **Endpoints centralizados** - Um endpoint para cada agente
- ✅ **Porta única (8000)** - Todos os serviços acessíveis via uma porta
- ✅ **Padrão Google ADK** - Arquitetura baseada em BaseAgent, Tools, Events
- ✅ **Multi-Agente** - Sistema coordenado de agentes especializados
- ✅ **OpenAI GPT-4** - IA conversacional natural
- ✅ **Supabase** - Banco de dados PostgreSQL
- ✅ **N8N** - Integração com WhatsApp via workflow automation

---

## 🤖 Agentes Disponíveis

### 1. **Maria Agent** 👩‍💼
- **Endpoint:** `POST /agents/maria`
- **Função:** Atendimento inicial, qualificação de leads
- **Características:**
  - Personalidade calorosa e amigável
  - Conhecimento completo do Espaço Vila do Sol
  - Responde perguntas sobre preços, capacidade, serviços
  - Usa OpenAI GPT-4 para respostas naturais

### 2. **Booking Agent** 📅
- **Endpoint:** `POST /agents/booking`
- **Função:** Criação e gerenciamento de reservas
- **Características:**
  - Extrai data, horário, número de convidados
  - Cria registros no Supabase
  - Valida informações antes de confirmar
  - Tool: `create_booking_supabase`

### 3. **Report Agent** 📊
- **Endpoint:** `POST /agents/report`
- **Função:** Relatórios e notificações
- **Características:**
  - Gera resumos de conversas
  - Envia alertas para empresa
  - Documentação de interações

### 4. **Host Agent** 🎯
- **Endpoint:** `POST /agents/host`
- **Função:** Orquestrador de agentes
- **Características:**
  - Classifica mensagens automaticamente
  - Roteia para o agente apropriado
  - Coordena fluxo multi-agente

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.8+
- OpenAI API Key
- Supabase Account
- (Opcional) N8N + WAHA para WhatsApp

### Configuração

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/guimileib/FastCamp.git
   cd FastCamp/card12
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as variáveis de ambiente:**
   ```bash
   cp .env.example .env
   ```

   Edite `.env`:
   ```env
   OPENAI_API_KEY=sk-proj-...
   OPENAI_MODEL=gpt-4
   
   SUPABASE_URL=https://seu-projeto.supabase.co
   SUPABASE_KEY=eyJhbGci...
   
   WHATSAPP_PHONE_NUMBER=+5511999999999
   N8N_WEBHOOK_URL=http://localhost:5678
   
   API_HOST=0.0.0.0
   API_PORT=8000
   API_DEBUG=true
   ```

4. **Inicie o servidor:**
   ```bash
   python main.py
   ```

   Você verá:
   ```
   ============================================================
   🚀 Iniciando Party Agent API (Google ADK)
   ============================================================
   📱 WhatsApp: +5511999999999
   🔗 N8N Webhook: http://localhost:5678
   🌐 API Host: 0.0.0.0:8000

   📍 Endpoints disponíveis:
      - POST /webhook/whatsapp  (N8N Integration)
      - POST /agents/maria      (Maria Agent - ADK)
      - POST /agents/booking    (Booking Agent - ADK)
      - POST /agents/report     (Report Agent - ADK)
      - POST /agents/host       (Host Orchestrator - ADK)
      - GET  /agents/           (Lista todos os agentes)
   ============================================================
   ```

---

## 📍 Endpoints

### Base URL
```
http://localhost:8000
```

### Agentes (Google ADK)

#### 🤖 Maria Agent
```http
POST /agents/maria
Content-Type: application/json

{
  "message": "Olá, quanto custa alugar o espaço?",
  "user_id": "5511999999999@c.us",
  "user_name": "João Silva"
}
```

#### 📅 Booking Agent
```http
POST /agents/booking
Content-Type: application/json

{
  "message": "Quero reservar para 15/12 com 100 convidados",
  "user_id": "5511999999999@c.us",
  "user_name": "Maria Silva",
  "metadata": {
    "phone": "+5511999999999",
    "action": "create_booking"
  }
}
```

#### 📊 Report Agent
```http
POST /agents/report
Content-Type: application/json

{
  "message": "Gerar relatório desta conversa",
  "user_id": "5511999999999@c.us",
  "user_name": "Sistema"
}
```

#### 🎯 Host Agent
```http
POST /agents/host
Content-Type: application/json

{
  "message": "Olá, preciso de informações",
  "user_id": "5511999999999@c.us",
  "user_name": "Cliente"
}
```

#### 📋 Lista Agentes
```http
GET /agents/
```

### Webhook (N8N)

#### 📱 WhatsApp Webhook
```http
POST /webhook/whatsapp
Content-Type: application/json

{
  "chat_id": "5511999999999@c.us",
  "from": "5511999999999@c.us",
  "message": "Olá",
  "pushname": "João Silva",
  "session": "default"
}
```

### Utilitários

#### 🏥 Health Check
```http
GET /health
```

#### 📖 Swagger UI
```
http://localhost:8000/docs
```

---

## 🧪 Exemplos de Teste

### PowerShell (Windows)

```powershell
# Maria Agent
$body = @{
    message = "Olá, quanto custa?"
    user_id = "test@c.us"
    user_name = "Teste"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/agents/maria" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### cURL (Linux/Mac)

```bash
# Maria Agent
curl -X POST http://localhost:8000/agents/maria \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Olá, quanto custa?",
    "user_id": "test@c.us",
    "user_name": "Teste"
  }'

# Booking Agent
curl -X POST http://localhost:8000/agents/booking \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Reservar 15/12 com 100 convidados",
    "user_id": "test@c.us",
    "user_name": "Teste",
    "metadata": {"phone": "+5511999999999"}
  }'

# Listar Agentes
curl http://localhost:8000/agents/
```

---

## 🏗️ Arquitetura Google ADK

### Componentes Principais

```python
# Base Agent
class BaseAgent(ABC):
    async def execute(context: AgentContext) -> AgentResponse
    async def run(payload: dict) -> dict
    def emit_event(event_type, data)
    def add_tool(tool: Tool)

# Agent Context
@dataclass
class AgentContext:
    session_id: str
    user_id: str
    user_name: str
    message: str
    metadata: Dict
    history: List

# Agent Response
@dataclass
class AgentResponse:
    agent_name: str
    response: str
    confidence: float
    events: List[AgentEvent]
    metadata: Dict
    tools_used: List[str]

# Tool
@dataclass
class Tool:
    name: str
    description: str
    parameters: Dict
    function: Callable

# Event Type
class EventType(Enum):
    START = "start"
    MESSAGE = "message"
    TOOL_CALL = "tool_call"
    TOOL_RESULT = "tool_result"
    ERROR = "error"
    COMPLETE = "complete"
```

### Estrutura de Arquivos

```
card12/
├── main.py                         # FastAPI app entry point
├── .env                            # Environment variables
├── requirements.txt                # Python dependencies
│
├── app/
│   ├── agents/
│   │   ├── base_agent.py          # Base ADK (BaseAgent, Tool, Event)
│   │   ├── maria_agent/
│   │   │   └── agent.py           # MariaAgent(BaseAgent)
│   │   ├── booking_agent/
│   │   │   └── agent.py           # BookingAgent(BaseAgent)
│   │   ├── report_agent/
│   │   │   └── agent.py           # ReportAgent
│   │   └── host_agent/
│   │       └── agent.py           # Host orchestrator
│   │
│   └── routes/
│       ├── agents_routes.py       # Endpoints ADK (/agents/*)
│       └── webhook_routes.py      # N8N webhook
│
└── docs/
    ├── ARQUITETURA_ADK.md         # Documentação completa
    ├── MAPA_ENDPOINTS.md          # Mapa de endpoints
    ├── RESUMO_IMPLEMENTACAO.md    # Resumo executivo
    ├── COMPARACAO_ANTES_DEPOIS.md # Comparação
    └── EXEMPLOS_TESTE.md          # Exemplos práticos
```

---

## 📊 Fluxo de Execução

```
1. Cliente → HTTP Request → POST /agents/maria
                             ↓
2. agents_routes.py recebe AgentRequest
                             ↓
3. Converte para payload compatível
                             ↓
4. Chama maria_agent.run(payload)
                             ↓
5. run() cria AgentContext
                             ↓
6. run() chama execute(context)
                             ↓
7. execute() processa com OpenAI GPT-4
                             ↓
8. execute() emite eventos (START, MESSAGE, COMPLETE)
                             ↓
9. execute() retorna AgentResponse
                             ↓
10. run() formata resposta compatível
                             ↓
11. agents_routes.py retorna JSON
```

---

## 🔗 Integração N8N + WhatsApp

### Fluxo WhatsApp

```
WhatsApp → WAHA → N8N → FastAPI:8000 → /webhook/whatsapp
                                              ↓
                                        Host Agent
                                              ↓
                                    ┌─────────┴─────────┐
                                    |                   |
                              Maria Agent      Booking Agent
                                    |                   |
                              OpenAI GPT-4         Supabase
```

### Configuração N8N

1. Webhook Trigger (WAHA)
2. HTTP Request → `http://host.docker.internal:8000/webhook/whatsapp`
3. HTTP Request → WAHA Send Message

---

## 📚 Documentação Completa

- **[ARQUITETURA_ADK.md](./ARQUITETURA_ADK.md)** - Arquitetura completa do sistema
- **[MAPA_ENDPOINTS.md](./MAPA_ENDPOINTS.md)** - Mapa visual dos endpoints
- **[RESUMO_IMPLEMENTACAO.md](./RESUMO_IMPLEMENTACAO.md)** - Resumo executivo
- **[COMPARACAO_ANTES_DEPOIS.md](./COMPARACAO_ANTES_DEPOIS.md)** - Comparação da estrutura
- **[EXEMPLOS_TESTE.md](./EXEMPLOS_TESTE.md)** - Exemplos práticos de teste

---

## 🛠️ Tecnologias

- **FastAPI** - Web framework
- **OpenAI GPT-4** - IA conversacional
- **Supabase** - PostgreSQL database
- **N8N** - Workflow automation
- **WAHA** - WhatsApp integration (NOWEB engine)
- **Python 3.8+** - Programming language
- **Uvicorn** - ASGI server

---

## 📝 Licença

MIT License

---

## 👨‍💻 Autor

**Guilherme Mileib**
- GitHub: [@guimileib](https://github.com/guimileib)
- Repository: [FastCamp](https://github.com/guimileib/FastCamp)

---

## 🎯 Roadmap

- [x] ✅ Base ADK implementada
- [x] ✅ Maria Agent com OpenAI
- [x] ✅ Booking Agent com Supabase
- [x] ✅ Endpoints centralizados
- [x] ✅ Documentação completa
- [ ] ⚠️ Report Agent ADK
- [ ] ⚠️ Autenticação (API Key)
- [ ] ⚠️ Rate limiting
- [ ] ⚠️ Logging estruturado
- [ ] ⚠️ Testes unitários
- [ ] ⚠️ CI/CD

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📞 Suporte

Para dúvidas ou suporte:
- Abra uma issue no GitHub
- Consulte a documentação em `/docs`
- Acesse o Swagger UI: http://localhost:8000/docs

---

**🎉 Party Agent API - Transformando atendimento em experiência!**
