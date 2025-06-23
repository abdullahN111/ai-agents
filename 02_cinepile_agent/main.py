from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents.run import RunConfig
from dotenv import load_dotenv
import os
import asyncio

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
    tracing_disabled=True
)


async def movie(movie_input: str) -> None:
    agent: Agent = Agent(name="Movie Quotes", instructions="When User said 1, your job is to provide a movie quote randomly with author of the quote and movie name. and if user said something else, you should reply Invalid input.")
    result = await Runner.run(agent, movie_input, run_config=config)
    print(result.final_output)


async def show(show_input: str) -> None:
    agent: Agent = Agent(name="Show Quotes", instructions="When User said 2, your job is to provide a show quote randomly with author of the quote and show name. and if user said something else, you should reply Invalid input.")
    result = await Runner.run(agent, show_input, run_config=config)
    print(result.final_output)


def main() -> None:
    options = ["Movie", "Show", "Exit"]
    print("\n<---Welcome to Cinepile Quote Generator--->\n")
    
    
    condition = True
    while condition:
        for index, option in enumerate(options):
            print(f"{index+1}. {option}")
            
        user_input: str = input("\nSelect something: ")
        
        if user_input == "1":
            asyncio.run(movie(user_input))
        
        elif user_input == "2":
            asyncio.run(show(user_input))
        
        elif user_input == "3":
            condition = False
            print('\n"I think this is the end of a beautiful friendship" - Neil, Tenet')
           
            
            
if __name__ == "__main__":
    main()