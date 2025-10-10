# 🧪 Exemplos de Teste - Endpoints ADK

## 🚀 Como Iniciar

```bash
cd "c:\Users\guilh\OneDrive\Área de Trabalho\FastCamp\card12"
python main.py
```

Aguarde até ver:
```
============================================================
🚀 Iniciando Party Agent API (Google ADK)
============================================================
📍 Endpoints disponíveis:
   - POST /agents/maria      (Maria Agent - ADK)
   - POST /agents/booking    (Booking Agent - ADK)
   ...
============================================================
```

---

## 📍 Exemplos com cURL (Windows PowerShell)

### 1. Maria Agent - Saudação

```powershell
$body = @{
    message = "Olá, bom dia!"
    user_id = "5511999999999@c.us"
    user_name = "João Silva"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/agents/maria" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

**Resposta esperada:**
```json
{
  "response": "Oi João! Bom dia! 😊 Tudo bem? Eu sou a Maria, do Espaço Vila do Sol! Como posso te ajudar hoje? 🎉",
  "agent": "maria_agent",
  "confidence": 0.85,
  "events": [
    {
      "type": "start",
      "timestamp": "2025-10-10T10:30:00.123456",
      "data": {
        "session_id": "abc123...",
        "user_id": "5511999999999@c.us",
        "message": "Olá, bom dia!"
      }
    },
    {
      "type": "message",
      "timestamp": "2025-10-10T10:30:00.234567",
      "data": {
        "user": "João Silva",
        "message": "Olá, bom dia!"
      }
    },
    {
      "type": "complete",
      "timestamp": "2025-10-10T10:30:02.345678",
      "data": {
        "response_length": 87,
        "tokens": 45
      }
    }
  ],
  "metadata": {
    "model_used": "gpt-4",
    "tokens_used": 45,
    "user_name": "João Silva"
  },
  "tools_used": []
}
```

---

### 2. Maria Agent - Pergunta sobre Preços

```powershell
$body = @{
    message = "Quanto custa alugar o espaço para uma festa de aniversário?"
    user_id = "5511888888888@c.us"
    user_name = "Maria Santos"
    metadata = @{
        phone = "+5511888888888"
    }
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8000/agents/maria" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

**Resposta esperada:**
```json
{
  "response": "Oi Maria! Que legal que você está interessada no nosso espaço para festa de aniversário! 🎂🎉\n\nO valor do aluguel varia conforme o dia da semana e período. Para te passar um orçamento preciso, preciso de algumas informações:\n\n📅 Qual a data que você está pensando?\n👥 Quantos convidados você espera?\n⏰ Qual período? (manhã, tarde, noite ou dia todo)\n\nAssim consigo te passar os melhores valores! 😊",
  "agent": "maria_agent",
  "confidence": 0.85,
  "events": [...],
  "metadata": {
    "model_used": "gpt-4",
    "tokens_used": 120
  },
  "tools_used": []
}
```

---

### 3. Booking Agent - Reserva com Data

```powershell
$body = @{
    message = "Quero reservar para dia 15/12 com 100 convidados para uma festa de aniversário"
    user_id = "5511777777777@c.us"
    user_name = "Pedro Oliveira"
    metadata = @{
        phone = "+5511777777777"
        action = "create_booking"
    }
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8000/agents/booking" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

**Resposta esperada:**
```json
{
  "response": "✅ Reserva criada com sucesso!\n\n📋 Número da reserva: #42\n📅 Data: 2025-12-15\n⏰ Horário: 18:00\n👥 Convidados: 100 pessoas\n🎉 Tipo: aniversário\n\nEm breve entrarei em contato para confirmar os detalhes e enviar o contrato! 📄✨",
  "agent": "booking_agent",
  "confidence": 0.95,
  "events": [
    {
      "type": "start",
      "timestamp": "...",
      "data": {...}
    },
    {
      "type": "tool_call",
      "timestamp": "...",
      "data": {
        "tool": "create_booking_supabase",
        "data": {
          "customer_name": "Pedro Oliveira",
          "customer_phone": "+5511777777777",
          "event_date": "2025-12-15",
          "event_time": "18:00",
          "guest_count": 100,
          "event_type": "aniversário",
          "status": "pending"
        }
      }
    },
    {
      "type": "tool_result",
      "timestamp": "...",
      "data": {
        "tool": "create_booking_supabase",
        "success": true
      }
    },
    {
      "type": "complete",
      "timestamp": "...",
      "data": {...}
    }
  ],
  "metadata": {
    "booking_created": true,
    "booking_id": 42,
    "booking_data": {
      "id": 42,
      "customer_name": "Pedro Oliveira",
      "customer_phone": "+5511777777777",
      "event_date": "2025-12-15",
      "event_time": "18:00",
      "guest_count": 100,
      "event_type": "aniversário",
      "status": "pending",
      "created_at": "2025-10-10T10:30:00.000Z"
    }
  },
  "tools_used": ["create_booking_supabase"]
}
```

---

### 4. Booking Agent - Informações Incompletas

```powershell
$body = @{
    message = "Quero fazer uma reserva"
    user_id = "5511666666666@c.us"
    user_name = "Ana Costa"
    metadata = @{
        phone = "+5511666666666"
    }
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8000/agents/booking" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

**Resposta esperada:**
```json
{
  "response": "Ok! Para confirmar sua reserva, preciso de mais alguns detalhes:\n\n❓ data do evento\n❓ quantidade de convidados\n\nPode me passar essas informações? 😊",
  "agent": "booking_agent",
  "confidence": 0.7,
  "events": [...],
  "metadata": {
    "missing_info": ["data do evento", "quantidade de convidados"],
    "booking_info": {
      "event_date": null,
      "event_time": "18:00",
      "guest_count": null,
      "event_type": "festa",
      "customer_name": "Ana Costa",
      "customer_phone": "+5511666666666"
    }
  },
  "tools_used": []
}
```

---

### 5. Host Agent - Roteamento Automático

```powershell
$body = @{
    message = "Olá, tudo bem?"
    user_id = "5511555555555@c.us"
    user_name = "Carlos Mendes"
    metadata = @{
        phone = "+5511555555555"
    }
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8000/agents/host" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

**Resposta esperada:**
```json
{
  "response": "Oi Carlos! Tudo bem sim! E você? 😊 Eu sou a Maria, do Espaço Vila do Sol...",
  "agent": "maria_agent",
  "confidence": 0.7,
  "events": [],
  "metadata": {
    "routed_to": "maria_agent",
    "routing_reason": "Atendimento geral ou saudação"
  },
  "tools_used": []
}
```

---

### 6. Listar Todos os Agentes

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/agents/" -Method Get
```

**Resposta esperada:**
```json
{
  "agents": [
    {
      "name": "maria_agent",
      "endpoint": "/agents/maria",
      "description": "Agente de atendimento e qualificação de leads",
      "capabilities": [
        "Saudações e atendimento inicial",
        "Informações sobre o espaço",
        "Qualificação de leads",
        "Respostas personalizadas"
      ]
    },
    {
      "name": "booking_agent",
      "endpoint": "/agents/booking",
      "description": "Agente de agendamento e reservas",
      "capabilities": [
        "Extração de data/horário/convidados",
        "Criação de reservas no Supabase",
        "Confirmação de agendamentos",
        "Validação de informações"
      ]
    },
    {
      "name": "report_agent",
      "endpoint": "/agents/report",
      "description": "Agente de relatórios e notificações",
      "capabilities": [
        "Geração de relatórios",
        "Envio de notificações",
        "Resumo de conversas",
        "Alertas para empresa"
      ]
    },
    {
      "name": "host_agent",
      "endpoint": "/agents/host",
      "description": "Orquestrador de agentes (roteamento inteligente)",
      "capabilities": [
        "Classificação de mensagens",
        "Roteamento para agentes",
        "Coordenação multi-agente",
        "Gerenciamento de fluxo"
      ]
    }
  ],
  "architecture": "Google ADK (Agent Development Kit)",
  "port": 8000,
  "version": "2.0.0"
}
```

---

### 7. Health Check

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
```

**Resposta esperada:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "agent": "Party Agent",
  "n8n_configured": true
}
```

---

## 📍 Exemplos com cURL (Linux/Mac)

### Maria Agent

```bash
curl -X POST http://localhost:8000/agents/maria \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Olá, quanto custa?",
    "user_id": "5511999999999@c.us",
    "user_name": "João Silva"
  }'
```

### Booking Agent

```bash
curl -X POST http://localhost:8000/agents/booking \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Quero reservar 15/12 com 100 convidados",
    "user_id": "5511999999999@c.us",
    "user_name": "Pedro Oliveira",
    "metadata": {
      "phone": "+5511999999999",
      "action": "create_booking"
    }
  }'
```

### Listar Agentes

```bash
curl http://localhost:8000/agents/
```

---

## 🌐 Swagger UI (Interface Visual)

Acesse: **http://localhost:8000/docs**

### Como testar no Swagger:

1. Abra http://localhost:8000/docs
2. Localize a seção **"Agents (ADK)"**
3. Clique em **"POST /agents/maria"**
4. Clique em **"Try it out"**
5. Preencha o JSON de exemplo:
   ```json
   {
     "message": "Olá, quanto custa?",
     "user_id": "test@c.us",
     "user_name": "Teste"
   }
   ```
6. Clique em **"Execute"**
7. Veja a resposta abaixo

---

## 📊 Casos de Teste Completos

### Caso 1: Atendimento Inicial → Qualificação → Reserva

**Passo 1: Saudação (Maria Agent)**
```powershell
$body = @{
    message = "Oi, boa tarde!"
    user_id = "cliente1@c.us"
    user_name = "Lucas Silva"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/agents/maria" `
    -Method Post -ContentType "application/json" -Body $body
```

**Passo 2: Pergunta sobre Espaço (Maria Agent)**
```powershell
$body = @{
    message = "Quero saber sobre o espaço, quantas pessoas cabem?"
    user_id = "cliente1@c.us"
    user_name = "Lucas Silva"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/agents/maria" `
    -Method Post -ContentType "application/json" -Body $body
```

**Passo 3: Solicitar Reserva (Booking Agent)**
```powershell
$body = @{
    message = "Quero reservar para 20/12 com 80 convidados"
    user_id = "cliente1@c.us"
    user_name = "Lucas Silva"
    metadata = @{
        phone = "+5511999887766"
        action = "create_booking"
    }
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8000/agents/booking" `
    -Method Post -ContentType "application/json" -Body $body
```

---

### Caso 2: Uso do Host Agent (Roteamento Automático)

**Passo 1: Mensagem Ambígua**
```powershell
$body = @{
    message = "Olá, preciso de informações"
    user_id = "cliente2@c.us"
    user_name = "Fernanda Costa"
    metadata = @{
        phone = "+5511888776655"
    }
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8000/agents/host" `
    -Method Post -ContentType "application/json" -Body $body
```
→ Roteará para **Maria Agent**

**Passo 2: Mensagem de Reserva**
```powershell
$body = @{
    message = "Quero agendar para sábado próximo"
    user_id = "cliente2@c.us"
    user_name = "Fernanda Costa"
    metadata = @{
        phone = "+5511888776655"
    }
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8000/agents/host" `
    -Method Post -ContentType "application/json" -Body $body
```
→ Roteará para **Booking Agent**

---

## 🔍 Verificar Logs do Servidor

Enquanto testa, observe o terminal onde o servidor está rodando:

```
📍 Endpoint /agents/maria chamado por João Silva
🤖 Maria Agent: Processando mensagem de João Silva
   Mensagem: Olá, quanto custa?
   🔄 Chamando OpenAI (gpt-4)...
   ✅ Resposta OpenAI: Oi João! Tudo bem? 😊...
```

---

## ⚠️ Troubleshooting

### Erro: "Connection refused"

**Solução:** Verifique se o servidor está rodando:
```powershell
python main.py
```

### Erro: "404 Not Found"

**Solução:** Verifique o endpoint correto:
- ✅ http://localhost:8000/agents/maria
- ❌ http://localhost:8000/maria

### Erro: "422 Unprocessable Entity"

**Solução:** Verifique o JSON enviado. Campos obrigatórios:
- `message` (string)
- `user_id` (string)
- `user_name` (string, opcional mas recomendado)

### Erro: "500 Internal Server Error"

**Solução:** Verifique os logs do servidor para detalhes do erro.

---

## 📚 Próximos Passos

1. ✅ Testar todos os endpoints
2. ✅ Verificar respostas da OpenAI
3. ✅ Testar criação de bookings no Supabase
4. ⚠️ Adicionar histórico de conversa
5. ⚠️ Implementar autenticação
6. ⚠️ Adicionar rate limiting

---

## 🎯 Resumo dos Endpoints

| Endpoint | Método | Função | Teste Rápido |
|----------|--------|--------|--------------|
| `/agents/maria` | POST | Atendimento geral | `curl -X POST http://localhost:8000/agents/maria -H "Content-Type: application/json" -d '{"message": "Olá", "user_id": "test", "user_name": "Teste"}'` |
| `/agents/booking` | POST | Criar reservas | `curl -X POST http://localhost:8000/agents/booking -H "Content-Type: application/json" -d '{"message": "Reservar 15/12", "user_id": "test", "user_name": "Teste", "metadata": {"phone": "+5511999999999"}}'` |
| `/agents/report` | POST | Gerar relatórios | `curl -X POST http://localhost:8000/agents/report -H "Content-Type: application/json" -d '{"message": "Gerar relatório", "user_id": "test", "user_name": "Teste"}'` |
| `/agents/host` | POST | Roteamento | `curl -X POST http://localhost:8000/agents/host -H "Content-Type: application/json" -d '{"message": "Olá", "user_id": "test", "user_name": "Teste"}'` |
| `/agents/` | GET | Lista agentes | `curl http://localhost:8000/agents/` |
| `/health` | GET | Status | `curl http://localhost:8000/health` |
| `/docs` | GET | Swagger UI | Abrir no navegador |
