import os
from dotenv import load_dotenv

from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
from openai import AsyncOpenAI
from utils import models, database


set_tracing_disabled(True)
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_URL")
MODEL = "gemini-2.0-flash"


client = AsyncOpenAI(api_key=api_key, base_url=base_url)

model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=client,

)


@function_tool
def get_blog(id: int = None, title: str = None):
    """Takes id: int and title: str and returns blog with that id or title"""
    db_gen = database.get_db()
    db = next(db_gen)

    blog = None
    try:
        if id is not None:
            blog = db.query(models.Blog).filter(models.Blog.id == int(id)).first()
    except ValueError:
        blog = None

    if blog is None and title:
        blog = db.query(models.Blog).filter(models.Blog.title.ilike(f"%{title}%")).first()

    db_gen.close()

    if not blog:
        return "I am sorry, blog was not found. Please provide an existing blog id or title."

    return {
        "id": blog.id,
        "title": blog.title,
        "body": blog.body
    }


def get_response(user_input):
    
    agent = Agent(
        name="AI Blog Writer",
        instructions="""You are an AI-based blog writer and assistant.

Your responsibilities are:
1. When a user provides a topic, write a blog on that topic in paragraph form (around 250 words). Do not include any title or headings. At the end of the blog, add the author section in this format: "Written by Abdullah". Do not write anything else beyond the blog content.
2. After generating a blog, it will automatically be saved to the database with the provided topic as its title.
3. If the user wants to view a blog:
   - If they say something like "view blog 5" and 5 is a number, use `get_blog` with `id=5`.
   - If they say something like "view blog Babar Azam", use `get_blog` with `title='Babar Azam'`.
4. When returning a blog, just show the `title` and `body` clearly (no labels like 'Title:' or 'Body:'). End your response cleanly.

Respond only with the blog or blog content — no extra commentary.
.
""",
        model=model,
        tools=[get_blog]
    )
    return Runner.run_sync(agent, user_input)



