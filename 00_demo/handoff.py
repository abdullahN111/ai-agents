import asyncio

from agents import Agent, Runner, handoff

from agent_config import MyRunHook, config


news_headlines = Agent(name="News Headlines Agent", instructions="You are a news headlines agent, you will generate demo news headlines when asked.")

news_bulletin = Agent(name="News Bulletin Agent", instructions="You are a news Bulletin agent, you will give briefing on the headlines.")

news_headlines_agent = handoff(
    agent=news_headlines,
    
)

news_bulletin_agent = handoff(
    agent=news_bulletin,
    
)

news_agent = Agent(name="News Agent", instructions="You are a news agent your job is to give news to user, first create a headlines for the news using news_headlines_agent and then use news_bulletin_agent to give briefing", handoffs=[news_headlines_agent, news_bulletin_agent])

async def main():
    runner = await Runner.run(news_agent, "Tell me the news about crime rate in north carolina", run_config=config, hooks=MyRunHook())
    print(runner.final_output)
    
if __name__ == "__main__":
    asyncio.run(main())

