import os
from dotenv import load_dotenv

from agents import OpenAIChatCompletionsModel, SQLiteSession
from openai import AsyncOpenAI
# from agents.extensions.models.litellm_model import LitellmModel

load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_URL")
MODEL = "gemini-2.5-flash"
session = SQLiteSession("atm_session_22")

client = AsyncOpenAI(api_key=api_key, base_url=base_url)

model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=client,
)

# model = LitellmModel(
#     model=MODEL,
#     base_url=base_url,
#     api_key=api_key,
# )
