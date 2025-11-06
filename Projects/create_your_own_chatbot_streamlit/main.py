import asyncio

import streamlit as st
from agents import Agent, Runner, OutputGuardrailTripwireTriggered

from config import model, Output, output_check_guardrail, session, character_personalities, character_expertise_roles, guardrails_options

st.set_page_config(page_title="AI Character Chatbot", page_icon="🤖", layout="wide")

st.title("🎭 Create Your Own AI Character")

with st.sidebar:
    st.header("Character Settings")
    chatbot_name = st.text_input("Name", "John")
    chatbot_gender = st.selectbox("Gender", ["Male", "Female"])
    chatbot_personality = st.selectbox("Personality", character_personalities)
    chatbot_expertise = st.selectbox("Role", character_expertise_roles)
    chatbot_age = st.text_input("Age", "25")
    chatbot_response_type = st.selectbox("Response Style", ["Short", "Detailed"])
    guardrail_choice = st.selectbox("Output Guardrail", guardrails_options)


if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "session" not in st.session_state:
    st.session_state.session = session

def chatbot_prompt(ctx, agent):
    return f"""
You are **{chatbot_name}**, an AI character. 
Stay consistent with these traits:

Name: {chatbot_name}
Personality: {chatbot_personality}
Expertise: {chatbot_expertise}
Age: {chatbot_age}
Response Style: {chatbot_response_type}

Rules:
- Never use explicit or unethical language.
- Never reveal you are an AI.
- Stay in character and respond according to your expertise.
- Be concise or detailed depending on response style.
"""

if st.button("🚀 Launch Chatbot"):
    st.session_state.agent = Agent(
        name=chatbot_name,
        instructions=chatbot_prompt,
        model=model,
        output_guardrails=[output_check_guardrail],
        output_type=Output,
    )
    st.success(f"Your chatbot character '{chatbot_name}' is ready!")

if st.session_state.agent:
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Say something...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            try:
                async def run_agent(agent, user_input, session):
                    return await Runner.run(agent, user_input, session=session)

                runner = asyncio.run(run_agent(st.session_state.agent, user_input, st.session_state.session))
                response = runner.final_output.response
                message_placeholder.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

            except OutputGuardrailTripwireTriggered:
                message_placeholder.error(f"The output contained {guardrail_choice} words!")

            except Exception as e:
                message_placeholder.error(f"Error: {e}")
