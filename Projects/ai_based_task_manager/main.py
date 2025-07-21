import os
import json
from typing import Any, Dict
from dotenv import load_dotenv

import asyncio
from pydantic import BaseModel

from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled, AgentHooks, Tool, RunContextWrapper
from openai import AsyncOpenAI

load_dotenv()
set_tracing_disabled(disabled=True)



api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_URL")
MODEL = "gemini-2.0-flash"
TASKS = "tasks.json"

if not api_key or not base_url:
    raise ValueError("GEMINI_API_KEY and BASE_URL must be set in the environment variables.")

class MyAgentHook(AgentHooks):
    def __init__(self, display_name: str):
        self.event_counter = 0
        self.display_name = display_name

    async def on_start(self, context: RunContextWrapper, agent: Agent) -> None:
        self.event_counter += 1
        print(f"\n--Loop counter {self.event_counter}: {agent.name} started.")

    async def on_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
        self.event_counter += 1
        print(
            f"\n--Loop counter {self.event_counter}: {agent.name} ended."
        )

    async def on_handoff(self, context: RunContextWrapper, agent: Agent, source: Agent) -> None:
        self.event_counter += 1
        print(
            f"\n--Loop counter {self.event_counter}: {source.name} handed off to {agent.name}"
        )

    async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool: Tool) -> None:
        self.event_counter += 1
        print(
            f"\n--Loop counter {self.event_counter}: {agent.name} started tool {tool.name}"
        )

    async def on_tool_end(
        self, context: RunContextWrapper, agent: Agent, tool: Tool, result: str
    ) -> None:
        self.event_counter += 1
        print(
            f"\n--Loop counter {self.event_counter}: {agent.name} ended tool {tool.name}"
        )

client = AsyncOpenAI(api_key=api_key, base_url=base_url)
model = OpenAIChatCompletionsModel(model=MODEL, openai_client=client)

@function_tool
def add_task(task_name: str, task_description: str, task_deadline: str):
    """Add task will take task_name, task_description and task_deadline and store it in json file"""
    tasks = []
    task_id = 101
    
    
    if os.path.exists(TASKS):
        with open(TASKS, "r") as file:
            try:
                tasks = json.load(file)
                if tasks:
                    task_id = tasks[-1]["id"] + 1
            except json.JSONDecodeError:
                tasks = []
                    
    task = {
        "id": task_id,
        "title": task_name,
        "description": task_description,
        "deadline": task_deadline
    }
    
    tasks.append(task)
    task_id +1
    
    with open(TASKS, "w") as file:
            json.dump(tasks, file, indent=2)
            return f"Task {task_id}: added successfully"


async def main():
    print("\n<---Welcome to AI Based Task Manage Platform--->\n")
    options = ["Add Task", "View Task", "Update Task", "Delete Task", "Exit"]
    
    agent = Agent(name="Task Manager Agent", instructions="You are a task manager agent your job is to add, view, update and delete the task based on user query, you can guide user about it but when performing crud operations please use tools. like if user asked for options so you will call view_tasks tool, similarly if user wants to add task he will give you title, description and deadline so you will add it using add_task tool, and if user wants to update the task he will give you same information and you will use update_task tool, lastly user will give you task id if he wants to delete the specific task and you will use delete_task tool.", model=model, hooks=MyAgentHook("Task Manager"), tools=[add_task])
    
    condition = True
    while condition:
        try:
            user_input = input("\nSay something: ")
            
        except:
            print("Invalid Input")
            
        try:
            response = await Runner.run(starting_agent=agent, input=user_input)
            print(response.final_output)
        except Exception as e:
            print(f"Server Error: {e}")
            
        if user_input == "quit" or user_input == "exit":
            print("\n--Thanks for using our Task Manager--")
            condition = False


if __name__ == "__main__":
    asyncio.run(main())
