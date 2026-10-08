import httpx
from urllib.parse import urlencode
from app.config import settings
from app.services.raga.mapping import map_payload_to_raga_query
from app.services.engines.base import EngineUnavailable

async def execute_handoff(payload: dict) -> dict:
    mode = settings.raga_mode
    mapped_query = map_payload_to_raga_query(payload)
    
    if mode == "link":
        url = f"{settings.raga_site_url}?{urlencode(mapped_query)}"
        return {"mode": "link", "url": url, "result": None}
        
    elif mode == "api":
        if not settings.raga_api_url:
            raise EngineUnavailable("Raga API URL not configured")
            
        async with httpx.AsyncClient() as client:
            try:
                headers = {"Authorization": f"Bearer {settings.raga_api_key}"}
                response = await client.post(
                    settings.raga_api_url, 
                    json=mapped_query, 
                    headers=headers,
                    timeout=10.0
                )
                response.raise_for_status()
                return {"mode": "api", "url": None, "result": response.json()}
            except Exception as e:
                raise EngineUnavailable(f"Failed to reach Raga service: {str(e)}")
                
    raise EngineUnavailable(f"Unknown Raga mode: {mode}")
