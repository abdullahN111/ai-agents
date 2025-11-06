import json
from typing import Optional, List
from datetime import datetime

from agents import function_tool, Agent, handoff
from pydantic import BaseModel

from config import config


def generate_unique_id():
    try:
        with open("sent.json", "r") as f:
            data = json.load(f)
        if data:
            return max(email["id"] for email in data) + 1
        else:
            return 1
    except (FileNotFoundError, json.JSONDecodeError):
        return 1
    
unique_id = generate_unique_id()


formatted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class Email(BaseModel):
    id: int
    sender: str = "you@example.com"
    recipient: str
    subject: str
    body: str
    timestamp: str
    labels: List[str] = []
    attachments: List[str] = []
    status: str
    


@function_tool
def get_emails() -> str:
    """Fetch a list of emails from a local JSON file. and format them for display."""
    print("\n📥 Your Inbox\n")
    try:
        with open("inbox.json", "r") as file:
            data = json.load(file)
            formatted_emails = []
            for email in data:
                sender_name = email["sender"].split(".com")[0]
                body = email["body"]
                formatted_emails.append(f"{email['id']}. {sender_name}: {body}")

            return "\n".join(formatted_emails)
    except FileNotFoundError:
        return json.dumps({"error": "emails.json file not found."})
    except json.JSONDecodeError:
        return json.dumps({"error": "Error decoding JSON from emails.json."})
    
@function_tool
def read_email(id: Optional[int] = None, sender: Optional[str] = None) -> str:
    """Fetch a single email from a local JSON file for read by giving an arg email id: int, or sender email: str. and format it for display."""
    print("\n📧 Email\n")
    try:
        with open("inbox.json", "r") as file:
            data = json.load(file)
           
        email = None
        if id is not None and sender:
            email = next((e for e in data if e["id"] == id and e["sender"] == sender), None)
        elif id is not None:
            email = next((e for e in data if e["id"] == id), None)
        elif sender:
            email = next((e for e in data if e["sender"] == sender), None)

        if not email:
            return f"Error: No email found for id={id}, sender={sender}."

        formatted_email = (
            f"\nEmail ID: {email['id']}\n"
            f"From: {email['sender']}\n"
            f"To: {email['recipient']}\n"
            f"Subject: {email['subject']}\n"
            f"Date: {email['timestamp']}\n"
            f"\nBody:\n{email['body']}\n\n"
            f"Labels: {', '.join(email.get('labels', [])) or 'None'}\n"
            f"Attachments: {', '.join(email.get('attachments', [])) or 'None'}\n"
        )

        return formatted_email
        
    except FileNotFoundError:
        return json.dumps({"error": "emails.json file not found."})
    except json.JSONDecodeError:
        return json.dumps({"error": "Error decoding JSON from emails.json."})
    
    
email_agent = Agent(name="Email Agent", instructions=f"""
                    You are an email creation agent. 
Your job is to take the recipient, subject, body, and optional labels/attachments from the user 
and generate a valid email that follows the Email schema, You have modify the body and make it professional and brief.
Rules:
- `id` must always be generated from {unique_id}.
- `sender` must always be "you@example.com". Never invent a different sender.
- `timestamp` will be from {formatted}.
- `status` will be "sent".
- Only fill `recipient`, `subject`, `body`, `labels`, and `attachments` based on the user input.
- Do not invent random ids, timestamps, or sender values.

                    """, output_type=Email, handoff_description="Email agent who will generate structured email based on query.")

email_agent_handoff = handoff(agent=email_agent)

