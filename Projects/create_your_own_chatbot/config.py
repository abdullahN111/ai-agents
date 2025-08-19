import os
from pydantic import BaseModel

from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_export_api_key, RunContextWrapper, GuardrailFunctionOutput, output_guardrail
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
MODEL = "gemini-2.5-flash"



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
        
set_tracing_export_api_key(openai_api_key)

client = AsyncOpenAI(api_key=gemini_api_key, base_url=gemini_base_url)
model = OpenAIChatCompletionsModel(model=MODEL, openai_client=client)


chatbot_name = input("\n🎭 What is the name of your Character? ")
chatbot_gender = input("🎭 What is the gender of your Character? Male/Female: ")
chatbot_personality = input("😇 What is the personality of your Character? i.e Supportive, Arrogant etc: ")
chatbot_expertise = input("📚 What is the expertise of your Character? i.e Math Tutor, Story Teller etc: ")
chatbot_age = input(f"🎂 What is the age of your Character? ")
chatbot_response = input("✍️ What kind or response you want? Short/Detailed: ")

guardrail_choice = input("🚨 Which output guardrail do you want? (explicit/offensive/vulgar/other): ").strip().lower()

chatbot_config = {
    "chatbot_name": chatbot_name,
    "chatbot_gender": chatbot_gender,
    "chatbot_personality": chatbot_personality,
    "chatbot_expertise": chatbot_expertise,
    "chatbot_age": chatbot_age,
    "chatbot_response_type": chatbot_response
}


def guardrail_prompt(ctx: RunContextWrapper, agent: Agent) -> str:
    return f"""
Check if a response is contains any {guardrail_choice} word.
"""


guardrail_agent = Agent(
    name="Output Checker",
    instructions=guardrail_prompt,
    output_type=OutputCheck,
    model=model,
)

@output_guardrail
async def output_check_guardrail(ctx: RunContextWrapper, agent: Agent, output: Output) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, output.response, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_valid,
    )