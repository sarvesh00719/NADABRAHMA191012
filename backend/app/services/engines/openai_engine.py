import os
from openai import AsyncOpenAI
from app.config import settings
from app.services.engines.base import EngineContext, EngineReply, ConversationEngine, EngineUnavailable

class OpenAIEngine:
    name: str = "openai"
    version: str = "gpt-4o-mini"
    
    def __init__(self):
        self.api_key = settings.openai_api_key
        
    async def reply(self, ctx: EngineContext) -> EngineReply:
        if not self.api_key:
            raise EngineUnavailable("OpenAI API key is missing")
            
        try:
            client = AsyncOpenAI(api_key=self.api_key)
            
            from app.services.safety import CONTENT_DIR
            rules_path = CONTENT_DIR / "counselor_rules.md"
            rules = ""
            if rules_path.exists():
                with open(rules_path, "r", encoding="utf-8") as f:
                    rules = f.read()
            
            stage_hints = {
                "listen": "Stage: listen. Invite the person to share. One open question.",
                "reflect": "Stage: reflect. Say back what you heard in one sentence, then a gentle check.",
                "explore": "Stage: explore. Ask one specific, open question about what matters most.",
                "suggest_activity": "Stage: suggest_activity. Offer one short activity as an option, not an instruction.",
                "wrap_up": "Stage: wrap_up. Thank them, give a one-sentence summary, suggest ending the session to review it."
            }
            hint = stage_hints.get(ctx.stage, "")
            system_instruction = f"{rules}\n\n{hint}\nLanguage: {ctx.language}"
            
            messages = [{"role": "system", "content": system_instruction}]
            for msg in ctx.history:
                role = "assistant" if msg["role"] == "assistant" else "user"
                messages.append({"role": role, "content": msg["content"]})
                
            response = await client.chat.completions.create(
                model=self.version,
                messages=messages,
                temperature=0.6,
                max_tokens=200,
            )
            
            text = response.choices[0].message.content
            if not text:
                raise EngineUnavailable("Empty response from OpenAI")
                
            return EngineReply(
                text=text.strip(),
                engine=self.name,
                model_version=self.version
            )
        except Exception as e:
            print(f"OPENAI ERROR: {str(e)}")
            raise EngineUnavailable(f"OpenAI generation failed: {str(e)}")
