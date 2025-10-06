import os
from dotenv import load_dotenv

from agents import OpenAIChatCompletionsModel, SQLiteSession, set_tracing_disabled
from openai import AsyncOpenAI

set_tracing_disabled(True)
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("GEMINI_BASE_URL")
MODEL = "gemini-2.5-flash"

if not api_key or not base_url:
    raise ValueError("GEMINI_API_KEY and BASE_URL must be set in the environment variables.")



client = AsyncOpenAI(api_key=api_key, base_url=base_url)
model = OpenAIChatCompletionsModel(model=MODEL, openai_client=client)