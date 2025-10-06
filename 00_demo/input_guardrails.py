from pydant import BaseModel
import asyncio

from agents import Agent, Runner, TResponseInputItem, input_guardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, RunContextWrapper

from agent_config import config


class ContainNumbers(BaseModel):
    is_contain_numbers: bool
    reasoning: str
    
numbers_guardrail_agent = Agent(name="Numbers Guardrail Agent", instructions="Determine if the input contains any numbers", output_type=ContainNumbers)

@input_guardrail
async def numbers_guardrail(wrapper: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    
    result = await Runner.run(starting_agent=numbers_guardrail_agent, input=input, run_config=config, context=wrapper.context)
    
    
    
    return GuardrailFunctionOutput(output_info=result.final_output, tripwire_triggered=result.final_output.is_contain_numbers)


async def main():
    agent = Agent(name="English Tutor", instructions="You are an English tutor, you help user learn english", input_guardrails=[numbers_guardrail])
    
    try:
        result = await Runner.run(starting_agent=agent, input="Hello, its been 2 days", run_config=config)
        
        print("✅ Request Successfull - ", result.final_output)
        
        
    except InputGuardrailTripwireTriggered:
        print("❌ Request failed - Numbers detected.")

    
if __name__ == "__main__":
    asyncio.run(main())


