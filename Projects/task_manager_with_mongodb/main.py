import asyncio

from agents import Agent, Runner, function_tool

from config import model, mongo_client


@function_tool
def create_task(title: str, desc: str = "") -> dict:
    """
    Create a new task in mongodb database
    
    Args:
        title: str (The title of the task)
        desc: str (Optional description of the task)
    Return:
        dict of newly created task
    """
    try:
        db = mongo_client["agent_db"]
        tasks = db["tasks"]
        
        new_task = {
            "title": title,
            "description": desc,
            "status": "pending"
        }
        
        result = tasks.insert_one(new_task)
        return {"id": str(result.inserted_id), **new_task}

    except Exception as e:
        raise ValueError(f"Error creating task: {e}")
    
@function_tool
def fetch_tasks() -> list:
    """Fetch all tasks from mongodb database"""
    
    try:
        db = mongo_client["agent_db"]
        tasks = db["tasks"]
        
        fetch_tasks = list(tasks.find())
        for task in fetch_tasks:
            task["_id"] = str(task["_id"])
        
        return fetch_tasks

    except Exception as e:
        raise ValueError(f"Error creating task: {e}")


async def main():
    print("\n<---Welcome to AI Based Task Manage Platform--->\n")
    
    agent = Agent(name="Task Manager Agent", instructions="You are a task manager agent your job is to add, view, update and delete the task based on user query, you can guide user about it but when performing crud operations please use tools. like if user asked for fetch or view tasks so you will call fetch_tasks tool, similarly if user wants to add task he will give you title, description(optional) so you will add it using create_task tool, lastly the user will give you task id if he wants to delete the specific task and you will use delete_task tool.", model=model, tools=[create_task, fetch_tasks])
    
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
