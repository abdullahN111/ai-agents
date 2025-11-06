import os
from pydantic import BaseModel
from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    RunContextWrapper,
    GuardrailFunctionOutput,
    output_guardrail,
    SQLiteSession,
    set_tracing_export_api_key
)
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class Output(BaseModel):
    response: str

class OutputCheck(BaseModel):
    is_valid: bool
    reasoning: str

openai_api_key = os.getenv("OPENAI_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_base_url = os.getenv("GEMINI_BASE_URL")


secrets = []
if not openai_api_key:
    secrets.append("OPENAI_API_KEY")
if not gemini_api_key:
    secrets.append("GEMINI_API_KEY")
if not gemini_base_url:
    secrets.append("GEMINI_BASE_URL")

if secrets:
    for secret in secrets:
        print(f"{secret} must be set in ENVIRONMENT VARIABLES.")
        
MODEL = "gemini-2.5-flash"
client = AsyncOpenAI(api_key=gemini_api_key, base_url=gemini_base_url)
model = OpenAIChatCompletionsModel(model=MODEL, openai_client=client)
session = SQLiteSession("chatbot_streamlit_session")
set_tracing_export_api_key(openai_api_key)

@output_guardrail
async def output_check_guardrail(ctx: RunContextWrapper, agent: Agent, output: Output) -> GuardrailFunctionOutput:
    
    return GuardrailFunctionOutput(output_info=None, tripwire_triggered=False)


character_personalities = [
    "Supportive",
    "Motivational",
    "Sarcastic",
    "Kind",
    "Calm and Logical",
    "Funny",
    "Arrogant",
    "Empathetic",
    "Serious and Professional",
    "Friendly",
    "Witty and Playful",
    "Philosophical",
    "Adventurous",
    "Mysterious",
    "Optimistic",
    "Realistic",
    "Chill and Relaxed",
    "Analytical",
    "Creative Thinker",
    "Inspiring Leader",
    "Teacher-like",
    "Cheerful",
    "Soft-spoken",
    "Confident",
    "Curious Explorer",
    "Dominant",
    "Rebellious",
    "Romantic",
    "Submissive",
]

character_expertise_roles = [
    "Teacher",
    "Student",
    "Doctor",
    "Engineer",
    "Software Developer",
    "Scientist",
    "Psychologist",
    "Lawyer",
    "Writer",
    "Journalist",
    "Artist",
    "Musician",
    "Entrepreneur",
    "Businessman",
    "Investor",
    "Life Coach",
    "Motivational Speaker",
    "Philosopher",
    "Historian",
    "Detective",
    "Chef",
    "Fitness Trainer",
    "Travel Guide",
    "Game Master",
    "Spiritual Mentor",
    "Poet",
    "Baby Sitter",
    "Nurse",
    "Politician",
    "Astronaut",
    "Researcher",
    "Fashion Designer",
    "Architect",
    "Maid",
    "Project Manager",
    "Data Analyst",
    "AI Researcher",
    "Therapist",
    "Content Creator",
    "Social Media Influencer",
    "Movie Director",
    "Comedian",
    "Storyteller",
    "Sports Coach"
]

guardrails_options = [
    "none",               
    "explicit",            
    "offensive",           
    "vulgar",              
    "violent",            
    "political",           
    "religious",           
    "medical",            
    "financial",           
    "illegal",             
    "bias_sensitive",      
]
