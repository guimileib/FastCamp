"""
Cliente Supabase usando REST API
Mais simples e confiável que conexão PostgreSQL direta
"""
import httpx
import os
from typing import Dict, Any, List, Optional
from loguru import logger
from dotenv import load_dotenv

load_dotenv()


class SupabaseClient:
    """Cliente simplificado para Supabase REST API"""
    
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        
        if not self.url or not self.key:
            logger.warning("SUPABASE_URL ou SUPABASE_KEY não configurados no .env")
        
        self.base_url = f"{self.url}/rest/v1"
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def insert(self, table: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insere um registro na tabela
        
        Exemplo:
        >>> await supabase.insert("conversations", {
        ...     "session_id": "whatsapp_123",
        ...     "user_id": "5511999999999",
        ...     "chat_id": "5511999999999@c.us"
        ... })
        """
        try:
            url = f"{self.base_url}/{table}"
            response = await self.client.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()[0] if response.json() else {}
        except Exception as e:
            logger.error(f"Erro ao inserir em {table}: {e}")
            return {}
    
    async def select(
        self, 
        table: str, 
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Busca registros na tabela
        
        Exemplo:
        >>> await supabase.select("conversations", 
        ...     filters={"session_id": "whatsapp_123"},
        ...     order_by="created_at.desc",
        ...     limit=10
        ... )
        """
        try:
            url = f"{self.base_url}/{table}"
            params = {"limit": limit}
            
            # Adiciona filtros
            if filters:
                for key, value in filters.items():
                    params[key] = f"eq.{value}"
            
            # Adiciona ordenação
            if order_by:
                params["order"] = order_by
            
            response = await self.client.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Erro ao buscar em {table}: {e}")
            return []
    
    async def update(
        self, 
        table: str, 
        filters: Dict[str, Any], 
        data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Atualiza registros na tabela
        
        Exemplo:
        >>> await supabase.update("conversations",
        ...     filters={"session_id": "whatsapp_123"},
        ...     data={"updated_at": "2025-10-10T12:00:00"}
        ... )
        """
        try:
            url = f"{self.base_url}/{table}"
            params = {}
            
            for key, value in filters.items():
                params[key] = f"eq.{value}"
            
            response = await self.client.patch(url, json=data, params=params, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Erro ao atualizar {table}: {e}")
            return []
    
    async def delete(self, table: str, filters: Dict[str, Any]) -> bool:
        """
        Deleta registros da tabela
        
        Exemplo:
        >>> await supabase.delete("messages",
        ...     filters={"id": "uuid-here"}
        ... )
        """
        try:
            url = f"{self.base_url}/{table}"
            params = {}
            
            for key, value in filters.items():
                params[key] = f"eq.{value}"
            
            response = await self.client.delete(url, params=params, headers=self.headers)
            response.raise_for_status()
            return True
        except Exception as e:
            logger.error(f"Erro ao deletar de {table}: {e}")
            return False
    
    async def rpc(self, function_name: str, params: Dict[str, Any] = None) -> Any:
        """
        Executa uma função PostgreSQL remota (RPC)
        
        Exemplo:
        >>> await supabase.rpc("get_conversation_stats", {"session_id": "whatsapp_123"})
        """
        try:
            url = f"{self.base_url}/rpc/{function_name}"
            response = await self.client.post(url, json=params or {}, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Erro ao executar RPC {function_name}: {e}")
            return None
    
    async def close(self):
        """Fecha o cliente HTTP"""
        await self.client.aclose()


# Singleton
supabase_client = SupabaseClient()
