import os
import asyncio

from fastapi import FastAPI
from agents import Agent, Runner, set_tracing_export_api_key

from app.routes import router as task_router
from app.tools import add_task, view_all_tasks, view_single_task, delete_task, greet_user
from utils.agent_config import model, session

# set_tracing_disabled(disabled=True)
tracing_api_key = os.environ["OPENAI_API_KEY"]
set_tracing_export_api_key(tracing_api_key)
    
app = FastAPI()
app.include_router(task_router)



async def main():
    
    print("\n<---Welcome to AI Based Task Manage Platform--->")
  
    
    
    
    agent = Agent(name="Task Manager Agent", instructions="""
    You are a Precise Task Manager Agent who can ADD, VIEW and DELETE Tasks based on user query, you will be using tools to perform your actions.
    
    Here is what you can do:
    
    - First you will greet the user and provide the user options using greet_user tool
    - If user wants to add a task you will call add_task
    - If user wants to view all tasks you will call view_all_tasks
    - If user wants to view single task by providing ID you will call view_single_task using that ID
    - If user wants to delete a task by providing ID you will call delete_task using that ID
    - If user wants to exit the program you will quietly exit without saying anything

    
    """, model=model, tools=[add_task, view_all_tasks, view_single_task, delete_task, greet_user])
    
    condition = True
    while condition:
        try:
            user_input = input("\nSay something: ")
            
        except:
            print("Invalid Input")
            
        if user_input == "quit" or user_input == "exit":
            print("\n--Thanks for using our Task Manager--")
            condition = False
        try:
            response = await Runner.run(starting_agent=agent, input=user_input, session=session)
            print(f'\n{response.final_output}\n')
        except Exception as e:
            print(f"Server Error: {e}")
            


if __name__ == "__main__":
    asyncio.run(main())


