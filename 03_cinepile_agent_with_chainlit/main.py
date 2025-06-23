import os
import chainlit as cl
from chainlit.user import User
from agents import Runner, Agent, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from dotenv import load_dotenv
from typing import Optional, Dict, cast

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")



def oauth_callback(provider_id: str, token: str, row_user_data: Dict[str, str], default_user: User) -> Optional[User]:
    """Handle the OAuth callback from github."""
    
    print(f"Provider: {provider_id}")
    print(f"User Data: {row_user_data}")
    
    return default_user

@cl.on_chat_start
async def start():
    
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
        model_provider=external_client,
        tracing_disabled=True
    )
    
    agent: Agent = Agent(name="Cinepile Agent", instructions="You are a cinepile quote agent, the user will ask you to generate a random quote from movie or a tv show with the quote author and show or movie title, the user will ask 1 for movie and 2 for tv show or simply they will say movie or show so you have generate a quote and after each quote the user again say something like movie or show you will again generate and aside from movie or show so you have to say sorry im just a cinepile agent", model=model)
    
    
    
    cl.user_session.set("chat_history", [])
    cl.user_session.set("config", config)
    cl.user_session.set("agent", agent)
    
    await cl.Message(content="Hello User, I am Cinepile Agent, Please select Movie or Show so I can generate random quote for you.").send()


@cl.on_message
async def main(message: cl.Message):
    msg = cl.Message(content="Generating...")
    await msg.send()
    
    agent: Agent = cast(Agent, cl.user_session.get("agent"))
    config: RunConfig = cast(RunConfig, cl.user_session.get("config"))
    
    history = cl.user_session.get("chat_history") or []
    
    history.append({
        "role": "user",
        "content": message.content
    })
    
    try:
        print("\n[CALLING_AGENT_WITH_CONTEXT]\n", history, "\n")
        result = Runner.run_sync(starting_agent=agent, input=history, run_config=config)
        
        response = result.final_output
        
        msg.content = response
        
        await msg.update()
        
        cl.user_session.set("chat_history", result.to_input_list())
        
        print(f"User: {message.content}")
        print(f"Assistant: {response}")
        
    except Exception as e:
        msg.content = f"Error: {str(e)}"
        await msg.update()
        print(f"Error: {str(e)}")