# Script de Teste - Sistema de Leads Quentes
import asyncio
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

async def test_host_agent():
    """Testa o Host Agent com lead quente"""
    
    print("=" * 60)
    print("🧪 TESTE DO SISTEMA DE LEADS QUENTES")
    print("=" * 60)
    
    try:
        # Import do host agent
        print("\n1️⃣ Importando Host Agent...")
        from app.agents.host_agent.agent import execute as host_execute
        print("   ✅ Import OK!")
        
        # Payload de teste (simula o que vem da rota)
        user_id = "5511999999999@s.whatsapp.net"
        payload = {
            "message": "Oi! Preciso reservar URGENTE para dia 20/12, festa de 100 pessoas. Quanto custa?",
            "user_name": "João Teste",
            "chat_id": user_id,
            "phone": user_id.split('@')[0],  # Extrai phone do user_id
            "context": {},
            "conversation_history": []
        }
        
        print("\n2️⃣ Enviando mensagem de teste:")
        print(f"   Mensagem: {payload['message'][:60]}...")
        
        # Executa
        print("\n3️⃣ Processando...")
        result = await host_execute(payload)
        
        print("\n4️⃣ Resultado:")
        print(f"   Agente escolhido: {result.get('orchestrator', {}).get('chosen_agent', 'N/A')}")
        print(f"   Temperatura: {result.get('orchestrator', {}).get('lead_analysis', {}).get('temperature', 'N/A')}")
        print(f"   Score: {result.get('orchestrator', {}).get('lead_analysis', {}).get('hot_score', 'N/A')}")
        print(f"   Notificou empresa: {result.get('report_sent', False)}")
        print(f"   Resposta: {result.get('message', result.get('response', 'N/A'))[:100]}...")
        
        print("\n" + "=" * 60)
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        
        return result
        
    except Exception as e:
        print(f"\n❌ ERRO NO TESTE:")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("\n🚀 Iniciando teste...\n")
    result = asyncio.run(test_host_agent())
    
    if result:
        print("\n✅ Sistema funcionando corretamente!")
    else:
        print("\n❌ Sistema com problemas!")
        sys.exit(1)
