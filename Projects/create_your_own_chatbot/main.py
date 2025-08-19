
from agents import Agent, Runner, RunContextWrapper, SQLiteSession, OutputGuardrailTripwireTriggered

from config import model, chatbot_config, output_check_guardrail, guardrail_choice, Output


session = SQLiteSession("chatbot_session")

def chatbot_prompt(ctx: RunContextWrapper, agent: Agent) -> str:
    return f"""
You are **{chatbot_config['chatbot_name']}**, an AI character. 
You must always stay consistent with the following traits:

Name: {chatbot_config['chatbot_name']}
Personality: {chatbot_config['chatbot_personality']}
Expertise: {chatbot_config['chatbot_expertise']}
Age: {chatbot_config['chatbot_age']}
Response Style: {chatbot_config['chatbot_response_type']}

Rules:
- Never try to take away the conversation into explicit, vulgar or unethical way.
- Never break character or reveal that you are an AI.
- Always respond in line with the given personality and expertise.
- Be concise or detailed depending on the chosen response type.
- If the user asks something outside your expertise, politely decline and redirect to your main role.

Remember: Every response should reflect your personality, expertise, and style consistently.
"""

chatbot_agent = Agent(name=chatbot_config["chatbot_name"], instructions=chatbot_prompt, model=model, output_guardrails=[output_check_guardrail], output_type=Output)


def main():
    conditions = ["Bye", "Exit", "Quit", "bye", "exit", "quit"]
    while True:
        user_input = input("\n🧑 You: ")
        lower_input = user_input.lower()


        if any(cond in lower_input for cond in conditions):
            print(f"\n{chatbot_config['chatbot_name']}: See you later! Bye.")
            break
            
            
        try:
            runner = Runner.run_sync(starting_agent=chatbot_agent, input=user_input, session=session)
            if chatbot_config["chatbot_gender"].lower() == "male" or chatbot_config["chatbot_gender"] == "Male":
                print(f"\n👨 {chatbot_config["chatbot_name"]}: {runner.final_output.response}")
                
            elif chatbot_config["chatbot_gender"].lower() == "female" or chatbot_config["chatbot_gender"] == "Female":
                print(f"\n👩 {chatbot_config["chatbot_name"]}: {runner.final_output.response}")
            
            else:
                print("Wrong Gender!")
                continue
            
        except OutputGuardrailTripwireTriggered:
            print(f"The output contain {guardrail_choice} words!")
            
        except Exception as e:
            print(f"\nError: {e}")



if __name__ == "__main__":
    main()