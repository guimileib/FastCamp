import httpx
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')

tables = ['bookings', 'reservas', 'reservations', 'agendamentos', 'events', 'calendario', 'leads']

print("🔍 Testando tabelas disponíveis no Supabase:\n")
for table in tables:
    try:
        response = httpx.get(
            f"{url}/rest/v1/{table}?limit=0",
            headers={"apikey": key, "Authorization": f"Bearer {key}"}
        )
        print(f"✅ {table}: {response.status_code}")
    except Exception as e:
        print(f"❌ {table}: {e}")
