import os

from agents import Agent, RunConfig, OpenAIChatCompletionsModel, RunContextWrapper, RunHooks
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("GEMINI_BASE_URL")
MODEL = "gemini-2.5-flash"

if not api_key or not base_url:
    raise ValueError("GEMINI_API_KEY and BASE_URL must be set in the environment variables.")


external_client = AsyncOpenAI(api_key=api_key, base_url=base_url)
model = OpenAIChatCompletionsModel(model=MODEL, openai_client=external_client)
config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

class MyRunHook(RunHooks):
    async def on_agent_start(self, context: RunContextWrapper[None], agent: Agent):
        print(f"Starting run for agent: {agent.name}")

    async def on_agent_end(self, context: RunContextWrapper[None], agent: Agent, final_output):
        print(f"Ending run for agent: {agent.name}")

    async def on_handoff(self, context: RunContextWrapper[None], from_agent: Agent, to_agent: Agent):
        print(f"Transferring from {from_agent.name} to {to_agent.name}")