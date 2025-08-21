import os

from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel, set_tracing_export_api_key
from openai import AsyncOpenAI

load_dotenv()

weather_api_key = os.getenv("WEATHER_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_base_url = os.getenv("GEMINI_BASE_URL")
weather_base_url = os.getenv("WEATHER_BASE_URL")

secrets = []
if not weather_api_key:
    secrets.append("WEATHER_API_KEY")
if not openai_api_key:
    secrets.append("OPENAI_API_KEY")
if not gemini_api_key:
    secrets.append("GEMINI_API_KEY")
if not gemini_base_url:
    secrets.append("GEMINI_BASE_URL")
if not weather_base_url:
    secrets.append("WEATHER_BASE_URL")


if secrets:
    for secret in secrets:
        print(f"{secret} must be set in ENVIRONMENT VARIABLES.")
        
set_tracing_export_api_key(openai_api_key)


client = AsyncOpenAI(api_key=gemini_api_key, base_url=gemini_base_url)
model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=client)