import os
import json

from agents import Agent, Runner, SQLiteSession

from tools import get_emails, read_email, email_agent_handoff, Email
from config import config

session = SQLiteSession("emailagent_session111")


def save_email(email: Email, file_path="sent.json"):
    """Append a new email to sent.json."""
    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
        else:
            data = []

        if not isinstance(data, list):
            data = []

        data.append(email.model_dump())

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

        print(f"\n✅ Email sent to {email.recipient}")

    except Exception as e:
        print(f"Error saving email: {e}")

def main():
    agent = Agent(name="Email Assistant", instructions="""
You are an intelligent Email Assistant.  
Your responsibilities include:  
- Listing all emails from the inbox in a clean, structured list.  
- Reading a specific email (by id or sender) and presenting it in a clear, professional format.  
- Sending new emails using the email agent handoff.  

Guidelines:  
- When listing emails, present them in a neat numbered list (ID, Sender, and a short preview of the body).  
- When reading an email, display all details (From, To, Subject, Date, Labels, Attachments, and Body) in a well-structured style.  
- Ensure clarity, professionalism, and consistency in formatting.  
""", tools=[get_emails, read_email], handoffs=[email_agent_handoff])
    
    
    print("\n--- Welcome to the Email Assistant! Type 'exit', 'quit', 'q', or 'bye' to leave. ---")
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in {"exit", "quit", "q", "bye"}:
                print("Exiting...")
                break
        except Exception as e:
            print(f"Input error: {e}")
            continue

        try:
            result = Runner.run_sync(agent, user_input, run_config=config)
    
            if isinstance(result.final_output, Email):
                save_email(result.final_output)
            else:
                print(result.final_output)
                
        except Exception as e:
            print(f"Error during agent execution: {e}")
            
if __name__ == "__main__":
    main()