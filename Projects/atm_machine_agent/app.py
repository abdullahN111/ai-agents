
import json
import asyncio

import streamlit as st
from streamlit_option_menu import option_menu
from agents import Agent, Runner, function_tool, set_tracing_disabled

from utils import model, session
from models import BankAccount

st.set_page_config(page_title="ATM Machine Agent", page_icon="🏧")

with st.sidebar:
    app = option_menu(
        menu_title="ATM Machine",
        options=["Login", "Check Balance", "Deposit", "Withdraw", "Change Pin"],
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "black"},
            "menu-title": {"color": "white", "font-size": "22px", "font-weight": "bold", "text-align": "center"},
            "nav-link": {"color": "white", "font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
            "nav-link-selected": {"background-color": "#02ab21"},
        },
    )


with open("accounts.json", "r") as f:
    account_data = json.load(f)

set_tracing_disabled(True)





accounts = [BankAccount(data["name"], data["pin"], data["balance"]) for data in account_data]
current_account = {"account": None}

@function_tool
def get_account(name: str, pin: int):
    for account in accounts:
        if account.name == name and str(account.pin) == str(pin):
            current_account["account"] = account
            return f"Account for {name} accessed successfully."
    return "Account not found."

@function_tool
def get_balance():
    account = current_account["account"]
    if not account:
        return "Please login first."
    return f"Your balance is {account.balance}"

@function_tool
def deposit(amount: int):
    account = current_account["account"]
    if not account:
        return "Please login first."
    return account.deposit(amount)

@function_tool
def withdraw(amount: int):
    account = current_account["account"]
    if not account:
        return "Please login first."
    return account.withdraw(amount)

@function_tool
def change_pin(prev_pin: int, new_pin: int):
    account = current_account["account"]
    if not account:
        return "Please login first."
    return account.change_pin(prev_pin, new_pin)

@function_tool
def greet():
    account = current_account["account"]
    if not account:
        return "Please login first."
    return account.greet_st()

agent = Agent(
    name="ATM Machine Agent",
    instructions="Authenticate using get_account, greet the user, then allow balance check, deposit, withdraw, or PIN change. Always ensure login first.",
    tools=[get_account, get_balance, deposit, withdraw, change_pin, greet],
    model=model,
)

async def run_agent(prompt: str):
    return await Runner.run(agent, prompt, session=session)

st.title("🚀 ATM Machine Interface")

if app == "Login":
    with st.form("login_form"):
        name = st.text_input("Name")
        pin = st.text_input("PIN", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            prompt = f"Login with name {name} and PIN {pin}"
            result = asyncio.run(run_agent(prompt))
            st.success(result.final_output)

elif app == "Check Balance":
    prompt = "Check my balance"
    result = asyncio.run(run_agent(prompt))
    st.write(result.final_output)

elif app == "Deposit":
    amount = st.number_input("Amount to deposit", min_value=1)
    if st.button("Deposit"):
        prompt = f"Deposit {amount}"
        result = asyncio.run(run_agent(prompt))
        st.success(result.final_output)

elif app == "Withdraw":
    amount = st.number_input("Amount to withdraw", min_value=1)
    if st.button("Withdraw"):
        prompt = f"Withdraw {amount}"
        result = asyncio.run(run_agent(prompt))
        st.success(result.final_output)

elif app == "Change Pin":
    with st.form("change_pin_form"):
        prev = st.text_input("Current PIN", type="password")
        new = st.text_input("New PIN", type="password")
        submitted = st.form_submit_button("Change PIN")
        if submitted:
            prompt = f"My previous pin was {prev}, and I want to change it to {new}"
            result = asyncio.run(run_agent(prompt))
            st.success(result.final_output)