import os
from pydantic import BaseModel

from agents import OpenAIChatCompletionsModel, set_tracing_export_api_key
from openai import AsyncOpenAI
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()

class Output(BaseModel):
    response: str
    
class OutputCheck(BaseModel):
    is_valid: bool
    reasoning: str
    
    
openai_api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_base_url = os.getenv("GEMINI_BASE_URL")
mongodb_url = os.getenv("MONGODB_URI")
MODEL = "gemini-2.5-flash"



secrets = []
if not openai_api_key:
    secrets.append("OPENAI_API_KEY")
if not gemini_api_key:
    secrets.append("GEMINI_API_KEY")
if not gemini_base_url:
    secrets.append("GEMINI_BASE_URL")
if not mongodb_url:
    secrets.append("MONGODB_URI")

if secrets:
    for secret in secrets:
        print(f"{secret} must be set in ENVIRONMENT VARIABLES.")
        
set_tracing_export_api_key(openai_api_key) # type: ignore

gemini_client = AsyncOpenAI(api_key=gemini_api_key, base_url=gemini_base_url)
model = OpenAIChatCompletionsModel(model=MODEL, openai_client=gemini_client)




mongo_client = MongoClient(mongodb_url, server_api=ServerApi("1")) # type: ignore

try:
    mongo_client.admin.command("ping")
    print("Database connected.")
    
except Exception as e:
    print(f"Error: {e}")
