import os
from agents import Runner, Agent, set_tracing_disabled
from dotenv import load_dotenv
import asyncio
from agents.extensions.models.litellm_model import LitellmModel

set_tracing_disabled(disabled=True)

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("BASE_URL")

MODEL = "openrouter/undi95/toppy-m-7b"

if not api_key:
    raise ValueError("OPENROUTER_API_KEY is not set in the environment variables.")


model = LitellmModel(
    model=MODEL,
    api_key=api_key,
    base_url=base_url,
)


async def main():
    
    agent = Agent(
        name="Attack On Titan Agent",
        instructions="You are a helpful assistant that can answer questions about the anime Attack on Titan. and you will not answer anything that is not related to Attack on Titan.",
        model=model,
    )
    
    try:
        result = await Runner.run(starting_agent=agent, input="Write lyrics of Attack on titan season 2 opening song sasageyo sasageyo.")
        print(result.final_output)
    except Exception as e:
        print("Error:", e)

    
    
if __name__ == "__main__":
    asyncio.run(main())