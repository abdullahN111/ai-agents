import os
from dotenv import load_dotenv
import json
import random
from typing import List, Dict

from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel, set_tracing_disabled
from openai import AsyncOpenAI
from pydantic import BaseModel

set_tracing_disabled(disabled=True)
load_dotenv()

class User(BaseModel):
    name: str
    health: int = 100 


api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_URL")
MODEL = "gemini-2.0-flash"

if not api_key or not base_url:
    raise ValueError("GEMINI_API_KEY and BASE_URL must be set in the environment variables.")


client = AsyncOpenAI(api_key=api_key, base_url=base_url)
model = OpenAIChatCompletionsModel(model=MODEL, openai_client=client)

user = User(name="Abdullah")
history: List[Dict] = []


@function_tool
def generate_event():
    """
    Randomly selects and returns the title of a game event from a JSON file (events.json).
    This function is used by the Narrator Agent when no specific event is provided by the user.
    """
    with open("events.json", "r") as file:
        events = json.load(file)
        random_event = random.choice(events) 
        return random_event["title"]

@function_tool
def choose_action(user_input: str, health: int = 100) -> Dict[str, str]:
    """
    Determines the result of a user action in the game.

    Acceptable actions: "Attack", "Retreat", "Heal", "Give Up".
    Returns a dictionary with updated message and health.
    """
    user_input = user_input.lower()

    if health < 1:
        return {"message": "You are too weak to act. You lose.", "health": str(health)}

    if user_input == "charge":
        return {"message": "You charged forward and struck the enemy!", "health": str(health)}
    elif user_input == "retreat":
        health = max(0, health - 50)
        return {"message": f"You fled the scene, regrouping. Your health: {health}", "health": str(health)}
    elif user_input == "heal":
        health = min(100, health + 50)
        return {"message": f"You used a potion and restored health. Your health: {health}", "health": str(health)}
    elif user_input == "give up":
        return {"message": "You have given up. Game over.", "health": "0"}
    else:
        return {"message": "Invalid action. Choose: Charge, Retreat, Heal, or Give Up.", "health": str(health)}

        
        
        
def main():
    print("\n<---Welcome to Game Master Agent--->")
    print("\n-------------------\n")
    print("Select an event.")
    
    
    while True:
            
        memory = "\n".join([f"User: {h['user']}\nAgent: {h['agent']}" for h in history])
        
        combat_agent = Agent(
    name="Combat Agent",
    instructions=f"""
        You are a combat agent. You will continue the story given by Narrator Agent. Your job is to combat with the enemy on behalf of the user. You will be continuing story onwards. 
        You will use the tool 'choose_action' to decide and execute actions like Charge, Heal, Retreat, or Give Up.
        "Conversation so far: {memory} Now continue the game from here.""",
    tools=[choose_action],
    handoff_description="Combat Agent is responsible for combat with the enemy"
)
                
        narrator_agent = Agent(name="Narrator Agent", instructions=f"""You are a narrator agent, when user ask you to give event/place you will narrate game story based on given event but if user did not provide you event you will call generate_event tool to get the event yourself and will generate story based on it. And user will go into it to play the game. User will face an enemy from the event and will charge on enemy. If user finds an enemy so please handoffs to Combat Agent to charge on enemy. Please keep the event story simple and full of thriller.
                               Conversation sa far: {memory}, now continue with conversation memory""", model=model, tools=[generate_event], handoffs=[combat_agent])
        
        
    
        
        
        
        
        try:
            user_input = input("\nSay something: ")
            
        except:
            print("Invalid Input!")
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("\nThank you for playing. Goodbye!\n")
            break
        
        try:
            response = Runner.run_sync(starting_agent=narrator_agent, input=user_input, context=user)
            print(response.final_output)
            print(response.last_agent.name)
            # result = eval(response.final_output)
            # if isinstance(result, dict) and "health" in result:
            #     user.health = int(result["health"])
            # print(f"(Updated Health: {user.health})")
    
           

        
            history.append({
        "user": user_input,
        "agent": response.final_output
    })
        except Exception as e:
            print("Server down: ",str(e))
            
    
    
if __name__ == "__main__":
    main()
