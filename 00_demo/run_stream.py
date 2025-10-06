import asyncio

from agents import Agent, Runner
from openai.types.responses import ResponseTextDeltaEvent

from agent_config import config


agent = Agent(name="Helpful Assistant", instructions="You are helpful assistant of user, answer his queries")

async def main():
    result = Runner.run_streamed(agent, "Hello tell me 5 jokes", run_config=config)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)

if __name__ == "__main__":
    asyncio.run(main())