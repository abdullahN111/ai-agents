from agents import Agent, Runner, function_tool
from agent_config import config

# --- Tools ---
@function_tool
def get_customer_info(customer_id: str) -> dict:
    # Fake DB lookup
    return {"id": customer_id, "name": "Alice", "balance": 120.50, "status": "active"}

# --- Agents ---

billing_agent = Agent(
    name="BillingAgent",
    instructions="You specialize in billing. Resolve any payment or refund related queries."
)

support_agent = Agent(
    name="SupportAgent",
    instructions=(
        "You are a customer support agent. "
        "If billing issue → handoff to BillingAgent. "
        "Otherwise, answer using reasoning or get_customer_info tool."
    ),
    tools=[get_customer_info],
    handoffs=[billing_agent],
)

# --- Orchestration (handoff) ---
async def run_support_query():
    result = await Runner.run(
        starting_agent=support_agent,
        input="My balance seems wrong, please fix my billing issue.",
        run_config=config,
    )
    print("Final:", result.final_output)

import asyncio
asyncio.run(run_support_query())
