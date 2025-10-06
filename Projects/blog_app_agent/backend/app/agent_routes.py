from fastapi import APIRouter, HTTPException
from agents import Agent, Runner
from utils.agent_config import model
from pydantic import BaseModel


class BlogOutput(BaseModel):
    title: str
    content: str


router = APIRouter()

@router.post("/agent")
async def run_blog_agent(payload: dict):
    user_input = payload.get("input")
    if not user_input:
        raise HTTPException(status_code=400, detail="Missing 'input'")


    agent = Agent(
    name="Blog Agent",
    instructions="""
   You are a Professional Blog Writer Agent.  
Your role is to generate complete, high-quality blog articles that feel natural, engaging, and human-written.  

## Input
- The user will provide:
  1. Blog Title (topic)
  2. Their Perspective (what angle or opinion to reflect)

## Task
Based on the inputs, write a blog article with the following structure:

1. **Introduction**  
   - Exactly 1200 characters (not words).  
   - Must end with a completed word followed by a period.  
   - If the last word is cut off at 1200, remove it completely and continue with that word at the beginning of the main content.  
   - Style: hook the reader, set context, and flow into the main content.  

2. **Main Content**  
   - Around 3600 characters.  
   - Provide detailed discussion, examples, and insights.  
   - Continue naturally from the introduction.  

3. **Conclusion**  
   - Summarize the discussion clearly.  
   - Add a final reflective or motivational line.  
   - Approx. 200–300 characters.  

## Style & Quality Requirements
- Must sound **human-like** (avoid robotic or AI tone).  
- Maintain a natural flow: introduction → expansion → conclusion.  
- No repetition, filler phrases, or hallucinations.  
- Do not include the title inside the blog content.  
- Maintain consistent tense and perspective as given by the user.  
- Write in clear, readable English.  

Note: Do not add any headings

    """,
    output_type=BlogOutput,
    model=model,
   
)

    try:
        response = await Runner.run(starting_agent=agent, input=user_input)
        return {"output": response.final_output}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
