from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled
from openai import AsyncOpenAI
from dotenv import load_dotenv
import json
import os

set_tracing_disabled(disabled=True)
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_URL")

MODEL = "gemini-2.0-flash"
SKILLS = "skills.json"


if not api_key or not base_url:
    raise ValueError("GEMINI_API_KEY and BASE_URL must be set in the environment variables.")


client = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url,
)

model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=client
)

@function_tool
def get_career_roadmap(career_name: str) -> str:
    """Return skill roadmap for a given career name."""
    with open(SKILLS, "r") as file:
        skills = json.load(file)
        for career in skills:
            if career["name"].lower() == career_name.lower():
                return f"The skill roadmap for {career['name']} is: {', '.join(career['skills'])}"
    return "Sorry, no matching career found in the roadmap."


career_agent = Agent(
    name="Career Agent",
    instructions="""You are Career Agent. Ask the user about their interests and strengths, then suggest the most relevant career paths. 
Only suggest career fields, do not explain the skills or jobs — let Skill Agent or Job Agent handle that.
""",
    model=model
)

skill_agent = Agent(
    name="Skill Agent",
    instructions="""You are Skill Agent. Based on the selected career field, provide a structured skill roadmap using the tool `get_career_roadmap`. 
Focus on guiding the user about what to learn, in what order, and how to improve their current skills.
Do not talk about specific job roles — that's the Job Agent's responsibility.""",
    model=model
)

job_agent = Agent(
    name="Job Agent",
    instructions="""You are Job Agent. Based on the selected career and skill set, suggest trending job titles, job responsibilities, and industries hiring for those roles. 
Focus on guiding the user to real-world job options related to their path. Do not explain skill-building — that's Skill Agent's job.
""",
    model=model
)


career_mentor_agent = Agent(
    name="Career Mentor",
    instructions="""
You are a career mentor who helps users explore career paths, learn required skills, and discover relevant job roles.

→ If the user shares their interests or strengths (e.g., "I like math and logic"), hand off to Career Agent to suggest career fields.
→ If the user mentions a career name (e.g., "Frontend Developer"), call the tool `get_career_roadmap` to provide the skill roadmap.
→ After the skill roadmap is shown, hand off to Skill Agent for learning strategies and improvement.
→ Once skills are discussed, hand off to Job Agent to explore real-world job roles and trends.

Only use tools or handoffs when appropriate. Always guide the user clearly through each step.
""",
    model=model,
    tools=[get_career_roadmap],
    handoffs=[career_agent, skill_agent, job_agent]
)


result = Runner.run_sync(career_mentor_agent, "tell me trending ai technologies for job")
print(result.final_output)