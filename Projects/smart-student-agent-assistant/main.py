
import asyncio
import os
from agents import Runner, Agent, AsyncOpenAI, OpenAIChatCompletionsModel, set_tracing_disabled
from dotenv import load_dotenv
from typing import Dict, List
import json
import re

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_URL")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")


client = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
)

model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=client,

    )


set_tracing_disabled(disabled=True)


TASKS_FILE = "tasks.json"



async def save_tasks() -> None:
    agent: Agent = Agent(name="Tasks Manager", instructions="""You are a task manager agent. Only accept tasks related to study. For each valid task name given by the student, return a JSON object with:

"name": "Task name"

"description": "A 800-characters explanation of the task"

"status": with "complete" and "delete"

Reject all non-study-related tasks. Remember not to write any other thing just return json object""", model=model)
    
    user_query = input("\nSay something: ")
    result = await Runner.run(agent, user_query)
    print(result.final_output)
    
    
    def extract_json_block(text: str) -> str:
        """Remove markdown backticks and extract the JSON block cleanly."""
        cleaned = re.sub(r"^```json|```$", "", text.strip(), flags=re.MULTILINE).strip()
        return cleaned

    try:
        raw = extract_json_block(result.final_output)
        task: Dict = json.loads(raw)
    except json.JSONDecodeError as e:
        print("Invalid JSON from agent.", str(e))
        return
    
    
    
    
    status = task.get("status")
    if isinstance(status, list) and status:
        task["status"] = status[0]
    elif isinstance(status, str):
        if " and " in status:
            task["status"] = status.split(" and ")[0].strip()
    else:
        print("Invalid status format.")
        return
        
    
    
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r", encoding="utf-8") as f:
            todos: List[Dict] = json.load(f)
    else:
        todos = []


    task["id"] = len(todos)+1
    todos.append(task)

    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2)

    print("Task saved successfully.")



async def display_tasks() -> None:
    print("\n---All Tasks---\n")
    if not os.path.exists(TASKS_FILE):
        print("No tasks found.")
        return
    
    with open(TASKS_FILE, "r", encoding="utf-8") as f:
        try:
            tasks: List[Dict] = json.load(f)
        except json.JSONDecodeError:
            print("Corrupted tasks.json")
            return
        
    for task in tasks:
        print(f"{task["id"]}. {task["name"]}")
        
   
    task_id = int(input("\nEnter task ID to get task details: "))

    for task in tasks:
        if task["id"] == task_id:
            print(f'\n>>> {task["id"]}. {task["name"]}\n')
            print(task["description"])
            print(f'\nStatus: {task["status"]}\n')
            break
    else:
        print("Task not found.") 


def main() -> None:
    
    options = ["Search & Save a Topic", "See Topics", "Exit"]
    print("\n<---Welcome to Smart Student Agent--->\n")
    condition = True
    while condition:
        for index, option in enumerate(options):
            print(f"{index+1}. {option}")
            
        user_input: str = input("\nSelect: ")
        
        if user_input == "1":
            asyncio.run(save_tasks())
        
        elif user_input == "2":
            asyncio.run(display_tasks())
        
        elif user_input == "3":
            condition = False
            print("\n---Good Bye---")


if __name__ == "__main__":
    main()