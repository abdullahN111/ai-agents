import io

from agents import Agent, Runner, function_tool
import pandas as pd

from agent_config import config

# --- Tools ---
@function_tool
def load_csv() -> str:
    df = pd.DataFrame({
        "customer": ["Alice", "Bob", "Charlie"],
        "spend": [120, 250, 75]
    })
    return df.to_csv(index=False)

@function_tool
def clean_data(csv: str) -> str:
    df = pd.read_csv(io.StringIO(csv))  
    df["spend"] = df["spend"].fillna(0).astype(int)
    return df.to_csv(index=False)

# --- Agent ---
etl_agent = Agent(
    name="ETLAgent",
    instructions=(
        "1. Load CSV using load_csv.\n"
        "2. Clean it using clean_data.\n"
        "3. Summarize spending trends in plain English."
    ),
    tools=[load_csv, clean_data],
)

# --- Run sync (batch mode) ---
result = Runner.run_sync(etl_agent, "Summarize customer spending", run_config=config)
print("📊 Final Report:", result.final_output)
