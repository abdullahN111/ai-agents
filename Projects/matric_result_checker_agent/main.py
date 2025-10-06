import asyncio

import streamlit as st
from agents import Agent, Runner, RunContextWrapper, function_tool

from utils.model_config import model
from utils.tools import get_tenth_result, get_ninth_result

st.set_page_config(page_title="Matric Result Agent", page_icon=":mortar_board:")

st.title(":newspaper: Your Matric Results are here!")
st.write("-------------------")
st.write(":white_check_mark: Check your result:")
user_class = st.selectbox("Select your class", ["10th", "9th"])
user_input = st.text_input("Enter your roll number")


def agent_instructions(ctx: RunContextWrapper, agent: Agent) -> str:
    return f"You are a Result Checker Agent. Your task is to check the matric results for students in class {user_class}. Provide the results in a clear and concise manner."

async def main():
    agent = Agent(name="Result Checker Agent", instructions=agent_instructions, model=model, tools=[get_tenth_result, get_ninth_result])
    
    if user_input:
        try:
           
            await Runner.run(agent, user_input)
    
        except ValueError:
            st.error("Please enter a valid roll number.")
    else:
        st.error("Please enter your roll number.")

if __name__ == "__main__":
    if st.button("Check Result"):
        asyncio.run(main())
