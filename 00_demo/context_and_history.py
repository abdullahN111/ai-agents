from dataclasses import dataclass
from typing import List
from agents import Agent, Runner, handoff, function_tool
from agents.extensions import handoff_filters
from agent_config import config

@dataclass
class SimpleCtx:
    user_name: str
    
@function_tool
def get_privacy_policy() -> str:
    """Return privacy policy"""
    return "Your info is safe with us"  
    
@function_tool
def get_contact_info() -> str:
    """Return Contact Information"""
    return "Abc Company, abc@gmail.com"  


# Another agent for billing
billing_agent = Agent(
    name="BillingAgent",
    instructions="Handle billing-related queries."
)


billing_handoff = handoff(
    agent=billing_agent,
)

# Specialist agent
faq_agent = Agent(
    name="FAQAgent",
    instructions="You answer FAQ questions.",
    tools=[get_privacy_policy, get_contact_info],
    handoffs=[billing_handoff]
)
ctx = SimpleCtx(user_name="Charlie")
res = Runner.run_sync(faq_agent, "tell me about privacy policy and contact info", context=ctx, run_config=config)
print("Final:", res.final_output)
