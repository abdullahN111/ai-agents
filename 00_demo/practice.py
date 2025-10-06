from agents import Agent, ModelSettings, Runner, function_tool
from pydant import BaseModel
from agent_config import config

@function_tool
def get_weather():
    "get the current weather"
    return "The weather in kaachi is sunny"

@function_tool
def get_news():
    "get the current news"
    return "The crime rate has increase in karchi"

agent = Agent(
    name="math_agent",
    instructions="You are a calculator. Always show step by step reasoning.",
    tools=[get_weather, get_news],
    tool_use_behavior="stop_on_first_tool",
    model_settings=ModelSettings(tool_choice="required")
)

runner = Runner.run_sync(agent, "Hello", run_config=config)
# print(runner.final_output)


class Reply(BaseModel):
    answer: str

agent = Agent(
    name="math_agent",
    instructions="You are a calculator. Always show step by step reasoning.",
    tools=[],
    output_type=Reply,
)

runner = Runner.run_sync(agent, "Hello", run_config=config)
# print(type(runner.final_output))

agent = Agent(
    name="Helpful Assistant",
    instructions="You are a Helpful Assistant.",
    tools=[],
    output_type=int,
)

runner = Runner.run_sync(agent, "Hello how are you", run_config=config)
# print(runner.final_output)


class Reply(BaseModel):
    is_math: bool
    answer: str

math_agent = Agent(
    name="math_agent",
    instructions="You are a calculator and math agent.",
    tools=[],
    output_type=Reply,
)

agent = Agent(name="Assistant", instructions="You are a helpful assistant. handoff to math agent if the query is about math", handoffs=[math_agent])
runner = Runner.run_sync(agent, "4 * 5 and then the outcome must be / by 2", run_config=config)
print(runner.final_output)
print(type(runner.final_output))
