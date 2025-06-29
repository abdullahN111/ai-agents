import os
from agents import Runner, Agent, OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI
from dotenv import load_dotenv
import asyncio

set_tracing_disabled(disabled=True)

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("BASE_URL")

MODEL = "mistralai/mistral-7b-instruct"

if not api_key:
    raise ValueError("OPENROUTER_API_KEY is not set in the environment variables.")


client = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url,
)

model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=client,
)

async def main():
    
    agent = Agent(
        name="Attack On Titan Agent",
        instructions="You are a helpful assistant that can answer questions about the anime Attack on Titan. and you will not answer anything that is not related to Attack on Titan.",
        model=model,
    )
    
    result = await Runner.run(starting_agent=agent, input="Write lyrics of Attack on titan season 2 opening song sasageyo sasageyo.")
    
    print(result.final_output)
    
    
if __name__ == "__main__":
    asyncio.run(main())