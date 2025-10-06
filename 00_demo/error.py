from agents import Agent, Runner, function_tool, RunContextWrapper, ModelSettings

from agent_config import config

@function_tool(
    failure_error_function=lambda ctx, e: f"Tool failed: {type(e).__name__}: {str(e)}"
)
def unsafe_divide(ctx: RunContextWrapper[None], numerator: float, denominator: float) -> float:
    # Might raise ZeroDivisionError
    return numerator / denominator

agent = Agent(
    name="SafeDivideAgent",
    instructions="Divide two numbers safely.",
    tools=[unsafe_divide],
    model_settings=ModelSettings(tool_choice="required")
)

# Test runs
# runner = Runner.run_sync(agent, "Compute 10 / 2", run_config=config)  # expected fine
runner = Runner.run_sync(agent, "Compute 10 / 0", run_config=config)  # should use the failure_error_function to produce a message

print(runner.final_output)  
