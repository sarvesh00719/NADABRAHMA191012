from app.services.engines.base import EngineContext, EngineReply, ConversationEngine

class StubEngine:
    name: str = "stub"
    version: str = "1.0"
    
    async def reply(self, ctx: EngineContext) -> EngineReply:
        replies = {
            "listen": "I'm listening. Tell me more.",
            "reflect": "It sounds like you're going through a lot. Is that right?",
            "explore": "What do you think is the hardest part of this?",
            "suggest_activity": "Would you like to try a quick breathing exercise?",
            "wrap_up": "Thank you for sharing. We can wrap up whenever you're ready."
        }
        return EngineReply(
            text=replies.get(ctx.stage, "I'm here for you."),
            engine=self.name,
            model_version=self.version
        )
