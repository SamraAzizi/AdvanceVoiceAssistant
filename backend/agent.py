from __future__ import annotations
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm
)
from livekit.agents.multimodal import MultimodalAgent
from dotenv import load_dotenv
from api import AssistantFnc
from prompts import WELCOME_MESSAGE, INSTRUCTIONS, LOOKUP_VIN_MESSAGE
import httpx
import os

load_dotenv()

# Load Ollama API config from environment variables
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")  # Default Ollama local server
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")  # Change to your preferred model

# Ollama Model Wrapper
class OllamaModel:
    def __init__(self, instruction, temperature=0.8):
        self.instruction = instruction
        self.temperature = temperature

    async def generate(self, prompt):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                OLLAMA_API_URL,
                json={"model": OLLAMA_MODEL, "prompt": prompt, "temperature": self.temperature},
            )
            response_json = response.json()
            return response_json.get("response", "Error generating response.")

# Initialize Ollama model
ollama_model = OllamaModel(instruction=INSTRUCTIONS)

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.SUBSCRIBE_ALL)
    await ctx.wait_for_participant()

    assistant_fnc = AssistantFnc()
    
    # Remove the assistant object using `self._session` because Ollama doesn't support it
    async def assistant_model(prompt):
        return await ollama_model.generate(prompt)

    # Send initial welcome message
    ctx.session.conversation.item.create(
    llm.ChatMessage(role="assistant", content=WELCOME_MESSAGE)
)
    print(dir(ctx.room))



    @ctx.room.on("user_speech_committed")
    async def on_user_speech_committed(msg: llm.ChatMessage):
        if isinstance(msg.content, list):
            msg.content = "\n".join("[image]" if isinstance(x, llm.ChatImage) else x for x in msg.content)

        if assistant_fnc.has_car():
            await handle_query(msg)
        else:
            await find_profile(msg)

    async def find_profile(msg: llm.ChatMessage):
        ctx.room.send_message(LOOKUP_VIN_MESSAGE(msg))

    async def handle_query(msg: llm.ChatMessage):
        response_text = await assistant_model(msg.content)  # Directly call Ollama model
        ctx.room.send_message(response_text)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
