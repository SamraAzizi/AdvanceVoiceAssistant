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
import json

load_dotenv()

# Load Ollama API config from environment variables
OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")

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

    async def assistant_model(prompt):
        return await ollama_model.generate(prompt)

    # ✅ **Fix: Use `ctx.room.local_participant.publish_data()` instead of `send_data()`**
    await ctx.room.local_participant.publish_data(
        data=json.dumps({
            "role": "assistant",
            "content": WELCOME_MESSAGE
        }).encode("utf-8"),
        kind=2,  # 2 = Reliable transmission
        topic="chat_message",
    )

    @ctx.room.on("user_speech_committed")
    async def on_user_speech_committed(msg: llm.ChatMessage):
        if isinstance(msg.content, list):
            msg.content = "\n".join("[image]" if isinstance(x, llm.ChatImage) else x for x in msg.content)

        if assistant_fnc.has_car():
            await handle_query(msg)
        else:
            await find_profile(msg)

    async def find_profile(msg: llm.ChatMessage):
        await ctx.room.local_participant.publish_data(
            data=json.dumps({
                "role": "assistant",
                "content": LOOKUP_VIN_MESSAGE
            }).encode("utf-8"),
            kind=2,
            topic="chat_message",
        )

    async def handle_query(msg: llm.ChatMessage):
        response_text = await assistant_model(msg.content)
        await ctx.room.local_participant.publish_data(
            data=json.dumps({
                "role": "assistant",
                "content": response_text
            }).encode("utf-8"),
            kind=2,
            topic="chat_message",
        )

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
