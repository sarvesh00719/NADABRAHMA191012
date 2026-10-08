import os
from google import genai
from app.config import settings
from app.services.engines.base import EngineContext, EngineReply, ConversationEngine, EngineUnavailable

class GeminiEngine:
    name: str = "gemini"
    version: str = settings.gemini_model or "gemini-3.8-flash"
    
    def __init__(self):
        self.api_key = settings.gemini_api_key
        
    async def reply(self, ctx: EngineContext) -> EngineReply:
        if not self.api_key:
            raise EngineUnavailable("Gemini API key is missing")
            
        try:
            client = genai.Client(api_key=self.api_key)
            
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
            
            checkin_info = ""
            if ctx.checkin:
                checkin_info = f"User Check-in prior to this session: Mood: {ctx.checkin.get('mood')}, Energy: {ctx.checkin.get('energy')}, Needs: {ctx.checkin.get('need')}."

            memory_info = ""
            if ctx.memory:
                memory_info = f"MEMORY OF PAST SESSIONS:\n{ctx.memory}\nUse this context to ask follow-ups about past sessions, check if they recovered or followed through on advice, and maintain an adaptive continuity!"

            
            # Feature-specific context overrides
            context_override = ""
            if ctx.goal == "yoga_sadhana":
                context_override = "CRITICAL CONTEXT: You are an expert Yoga and Pranayama instructor. You MUST strictly limit this conversation to teaching and discussing Yoga, Pranayama (Anulom Vilom, Bhramari), and proper posture. Do NOT act as a general therapist."
            elif ctx.goal == "digital_espresso":
                context_override = "CRITICAL CONTEXT: You are an AI neuro-focus coach. You MUST strictly limit this conversation to discussing high workload management, cognitive fatigue, and the neuroscience of focus. Recommend the user listen to the 40Hz Gamma wave 'Digital Espresso' audio to boost their concentration."
            elif ctx.goal == "sahasrara":
                context_override = "CRITICAL CONTEXT: You are an academic guide and meditation instructor. You MUST strictly limit this conversation to academics, studying, concentration, and pre-study meditation (like Omkar and focusing on the Sahasrara chakra)."
            
            if context_override:
                rules = rules + "`n`n" + context_override

            system_instruction = f"{rules}\n\n{hint}\n{checkin_info}\n\n{memory_info}\n\nLanguage: {ctx.language}"

            
            contents = []
            for msg in ctx.history:
                role = "model" if msg["role"] == "assistant" else "user"
                contents.append({"role": role, "parts": [{"text": msg["content"]}]})
                
            config = {
                "system_instruction": system_instruction,
                "temperature": 0.6,
                "max_output_tokens": 800,
            }
            
            import asyncio
            response = None
            last_error = None
            for attempt in range(3):
                try:
                    response = await client.aio.models.generate_content(
                        model=self.version,
                        contents=contents,
                        config=config
                    )
                    break
                except Exception as e:
                    last_error = e
                    if "503" in str(e) or "UNAVAILABLE" in str(e):
                        await asyncio.sleep(1.5 * (attempt + 1))
                        continue
                    raise e
                    
            if not response:
                raise last_error
                
            text = response.text
            if not text:
                raise EngineUnavailable("Empty response from Gemini")
                
            return EngineReply(
                text=text.strip(),
                engine=self.name,
                model_version=self.version
            )
        except Exception as e:
            print(f"GEMINI ERROR: {str(e)}"); raise EngineUnavailable(f"Gemini generation failed: {str(e)}")





