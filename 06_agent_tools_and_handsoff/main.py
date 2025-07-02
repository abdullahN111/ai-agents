from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

set_tracing_disabled(disabled=True)

load_dotenv()


@function_tool
def nextjs_projects():
    return "Next js projects names are Furniro, ResumeAbd, PortfolioAbd"

@function_tool
def python_projects():
    return "Python projects names are Cinepile Quotes, Library Management System, ATM Machine, Restaurant Service System"

@function_tool
def agents_ai_projects():
    return "Agents AI projects names are Cinepile Agent, Student Agent, Task Manager Agent"


@function_tool
def info():
    return "Abdullah lives in Korangi Karachi he have completed 14 years of education he is 22 years old he watched movies and shows and animes."

@function_tool
def family():
    return "Abdullah has 3 siblings and parents, he is the eldest of them. His siblings are Uzair, Sufyan, and Noorulain."


api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_URL")
MODEL = "gemini-2.0-flash"

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

client = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url,
)

model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=client
)

abdullah_family = Agent(
    name="Abdullah Family",
    instructions="This is Abdullah's family agent, it can answer questions about his family members.",
    model=model,
    tools=[family],
    handoff_description="Abdullah's family agent can provide details about his family members, including siblings and parents."
)

abdullah_info = Agent(
    name="Abdullah Info",
    instructions="This is Abdullah's info agent, it can answer questions about his personal information.",
    model=model,
    tools=[info],
    handoff_description="Abdullah's personal information agent can provide details about his background, education, and interests."
)


agent = Agent(
    name="Personal Assistant",
    instructions="You are a personal assistant of Abdullah, Abdullah is a developer He knows Next js and Python.",
    model=model,
    tools=[nextjs_projects, python_projects, agents_ai_projects],
    handoffs=[abdullah_family, abdullah_info]
)

user_input = input("Enter your message: ")

runner = Runner.run_sync(
    agent,
    user_input,
)

print(runner.final_output)