from pydant import BaseModel
import asyncio

from agents import Agent, Runner, output_guardrail, GuardrailFunctionOutput, OutputGuardrailTripwireTriggered, RunContextWrapper

from agent_config import config


class ErrorOutput(BaseModel):
    response: str

class ContainError(BaseModel):
    is_contain_error: bool
    reasoning: str
    
error_guardrail_agent = Agent(name="Error Guardrail Agent", instructions="Check if the response contains the word 'error'", output_type=ContainError)

@output_guardrail
async def error_guardrail(wrapper: RunContextWrapper[None], agent: Agent, output: ErrorOutput) -> GuardrailFunctionOutput:
    
    result = await Runner.run(starting_agent=error_guardrail_agent, input=f"Analyze this {output.response}", run_config=config, context=wrapper.context)
    
    
    
    return GuardrailFunctionOutput(output_info=result.final_output, tripwire_triggered=result.final_output.is_contain_error)


async def main():
    agent = Agent(name="English Tutor", instructions="You are an English tutor, you help user learn english", output_guardrails=[error_guardrail], output_type=ErrorOutput)
    
    try:
        result = await Runner.run(starting_agent=agent, input="im getting this error SyntaxError: expected ':'", run_config=config)
        
        print("✅ Response Successfull - ", result.final_output.response)
        
        
    except OutputGuardrailTripwireTriggered:
        print("❌ Response failed - Error detected.")

    
if __name__ == "__main__":
    asyncio.run(main())


