from dotenv import load_dotenv
import os
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

external_client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# agent: Agent = Agent(name="Translator", instructions="You are a transalator agent who can only translate roman urdu to english or english to roman urdu, and if someone ask other than this, you should reply, Sorry, my job is to translate only. and if they ask about translating other than urdu, tell them my job is to translate roman urdu to english or english to roman urdu.")

agent: Agent = Agent(name="Translator", instructions="You are a helpful assistant.")

user_input: str = input("Say something: ")

result = Runner.run_sync(agent, user_input, run_config=config)
print(result.final_output)