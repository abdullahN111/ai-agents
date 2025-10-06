from agents import Agent, Runner, function_tool, Handoff
import asyncio
from agent_config import config

@function_tool
def web_search(query: str) -> str:
    # Pretend search API
    return f"Results for {query}: AI Agents SDK, OpenAI docs, Panaversity resources."

writer_agent = Agent(
    name="WriterAgent",
    instructions="Write a short blog post from the research results. Output in Markdown format."
)
research_agent = Agent(
    name="ResearchAgent",
    instructions="You search the web using web_search tool and handoff results to WriterAgent.",
    tools=[web_search],
    handoffs=[writer_agent],
)


async def orchestrate():
    stream = Runner.run_streamed(
        starting_agent=research_agent,
        input="Write a blog on OpenAI Agent SDK",
        run_config=config
    )

    async for event in stream.stream_events():
        print("🔹 Stream event:", event)

    print("✅ Final:", stream.final_output)

asyncio.run(orchestrate())
