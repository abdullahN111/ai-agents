from agents import Agent, Runner
from dotenv import load_dotenv
import os

load_dotenv()
print("API Key loaded:", os.getenv("OPENAI_API_KEY"))

greeting_agent = Agent(
    name="Greeting Agent",
    instructions="You are a hello agent and your job is to greet user with nice and eligent words. You will only greet"
)

result = Runner.run_sync(greeting_agent, "Hello")

print(result.final_output)