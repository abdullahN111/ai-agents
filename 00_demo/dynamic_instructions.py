from agents import Agent, Runner
from agents import RunContextWrapper
from typing import Any

from agent_config import config

# Suppose this is your context type
class UserContext:
    def __init__(self, user_name: str, is_premium: bool):
        self.user_name = user_name
        self.is_premium = is_premium

# Define a dynamic instruction function
def dynamic_instructions(
    run_ctx: RunContextWrapper[UserContext],
    agent: Agent[UserContext]
) -> str:
    ctx = run_ctx.context
    premium_text = "You are a premium user." if ctx.is_premium else "You are a free user."
    return (
        f"Hello {ctx.user_name}. {premium_text} "
        "Answer the user’s questions politely and completely. If the user is premium, otherwise talk casually and rude"
    )

agent = Agent[UserContext](
    name="PersonalAgent",
    instructions=dynamic_instructions,
)

# Now run with a context
user_ctx = UserContext(user_name="Alice", is_premium=False)
result = Runner.run_sync(agent, "What should I eat today?", context=user_ctx, run_config=config)
print("Agent Output:", result.final_output)
