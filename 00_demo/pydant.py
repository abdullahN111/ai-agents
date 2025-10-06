from typing import Optional
from agents import Agent, Runner
from agent_config import config
from pydantic import BaseModel, Field

class UserInfo(BaseModel):
    name: str
    age: int
    email: Optional[str] = Field(None, description="User email, optional")

agent = Agent(
    name="UserInfoAgent",
    instructions="Extract name, age, and optionally email. Return JSON matching the schema.",
    output_type=UserInfo
)

result = Runner.run_sync(agent, "My name is Bob, I'm 32.", run_config=config)
# print(result.final_output)  
# -> an instance of UserInfo, e.g. UserInfo(name="Bob", age=32, email=None)


from pydantic import BaseModel
from agents import Agent, Runner, handoff

class BillingRequest(BaseModel):
    customer_id: str
    issue_type: str
    amount: float = 0.0  # default if not provided

billing_agent = Agent(
    name="BillingAgent",
    instructions="Resolve billing issues; input will follow BillingRequest schema.",
)

class SupportRequest(BaseModel):
    customer_id: str
    question: str

support_agent = Agent(
    name="SupportAgent",
    instructions="""
You’re a support agent. If the user is asking about billing, hand off to BillingAgent with structured input.
Otherwise, answer normally.
""",
    output_type=SupportRequest,  # for example output structure
    handoffs=[handoff(billing_agent)]
)

# Using it
res = Runner.run_sync(support_agent, "I need a refund, I paid extra for order #123 for $20.", run_config=config)
print(res.final_output)
# If handoff is triggered, then BillingAgent gets input validated to BillingRequest
