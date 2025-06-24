
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


TOPICS_FILE = "topics.json"



async def save_topic() -> None:
    agent: Agent = Agent(name="Tasks Manager", instructions="""You are a task manager agent. Only accept tasks related to study. For each valid task name given by the student, return a JSON object with:

"name": "Task name"

"description": "A 800-characters explanation of the task"

"status": with "complete" and "delete"

Reject all non-study-related tasks. Remember not to write any other thing just return json object""", model=model)
    
    user_query = input("\nSay something: ")
    result = await Runner.run(agent, user_query)

    
    
    def extract_json_block(text: str) -> str:
        """Remove markdown backticks and extract the JSON block cleanly."""
        cleaned = re.sub(r"^```json|```$", "", text.strip(), flags=re.MULTILINE).strip()
        return cleaned

    try:
        raw = extract_json_block(result.final_output)
        topic: Dict = json.loads(raw)
    except json.JSONDecodeError as e:
        print("Invalid JSON from agent.", str(e))
        return
    
    
    
    
    status = topic.get("status")
    if isinstance(status, list) and status:
        topic["status"] = status[0]
    elif isinstance(status, str):
        if " and " in status:
            topic["status"] = status.split(" and ")[0].strip()
    else:
        print("Invalid status format.")
        return
        
    
    
    if os.path.exists(TOPICS_FILE):
        with open(TOPICS_FILE, "r", encoding="utf-8") as f:
            topics: List[Dict] = json.load(f)
    else:
        topics = []


    topic["id"] = len(topics)+1
    topics.append(topic)

    with open(TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(topics, f, indent=2)

    print("\nTopic saved successfully.\n")



async def display_topics() -> None:
    print("\n---All Topics---\n")
    if not os.path.exists(TOPICS_FILE):
        print("No topics found.\n")
        return
    
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        try:
            topics: List[Dict] = json.load(f)
        except json.JSONDecodeError:
            print(f"Corrupted {TOPICS_FILE}")
            return
        
    for topic in topics:
        print(f"{topic["id"]}. {topic["name"]}")
        
   
    topic_id = int(input("\nEnter topic ID to get topic details: "))

    for topic in topics:
        if topic["id"] == topic_id:
            print(f'\n>>> {topic["id"]}. {topic["name"]}\n')
            print(topic["description"])
            print(f'\nStatus: {topic["status"]}\n')
            break
    else:
        print("Topic not found.") 

async def delete_topic():
    topic_id = int(input("\nEnter topic ID to delete a topic: "))
    
    with open(TOPICS_FILE, "r", encoding="utf-8") as f:
        try:
            topics: List[Dict] = json.load(f)
        except json.JSONDecodeError:
            print(f"Corrupted {TOPICS_FILE}")
            return
        
        for topic in topics:
            if topic_id == topic["id"]:
                topics.remove(topic)
                print(f"Topic {topic["name"]} removed successfully\n")
                
                
                with open(TOPICS_FILE, "w", encoding="utf-8") as f:
                    json.dump(topics, f, indent=4)
                return
    
        print(f"No topic found with ID {topic_id}\n")
    


def main() -> None:
    
    options = ["Search & Save Topic", "See Topics", "Delete Topic", "Exit"]
    print("\n<---Welcome to Smart Student Agent--->\n")
    condition = True
    while condition:
        for index, option in enumerate(options):
            print(f"{index+1}. {option}")
            
        user_input: str = input("\nSelect: ")
        
        if user_input == "1":
            asyncio.run(save_topic())
        
        elif user_input == "2":
            asyncio.run(display_topics())
        
        elif user_input == "3":
            asyncio.run(delete_topic())
        
        elif user_input == "4":
            print("\n---Good Bye---")
            condition = False
            
        else:
            print("Invalid Input! try again")


if __name__ == "__main__":
    main()