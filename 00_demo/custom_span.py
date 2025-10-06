import asyncio

from agents import Agent, Runner, custom_span, function_tool, trace

from agent_config import config

@function_tool 
def add(a: int, b: int) -> int: 
    with custom_span("add_function", data={"a": a, "b": b}): 
        return a + b
   
agent = Agent(name="Math Tutor", instructions="You are a math tutor. You help the user with math problems.", tools=[add]) 
    
async def main():
    with trace("AdderAgentTrace"): 
        result = await Runner.run(agent, "Add 12 and 8", run_config=config)
        print("Final Output:", result.final_output)

if __name__ == "__main__":
    asyncio.run(main())