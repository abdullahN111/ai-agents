import os

from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_export_api_key
from agents.run import RunConfig

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is not None:
    set_tracing_export_api_key(openai_api_key)
else:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")

gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_base_url = os.getenv("GEMINI_BASE_URL")
MODEL = "gemini-2.5-flash"


try:
    if not gemini_api_key or not gemini_base_url:
        raise ValueError("GEMINI_API_KEY or GEMINI_BASE_URL is not set in environment variables.")

    external_client = AsyncOpenAI(api_key=gemini_api_key, base_url=gemini_base_url)
    model = OpenAIChatCompletionsModel(openai_client=external_client, model=MODEL)
    config = RunConfig(model=model, model_provider=external_client)

except Exception as e:
    print(f"Error: {e}")


