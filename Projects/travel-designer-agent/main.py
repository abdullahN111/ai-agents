from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool, set_tracing_disabled
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
import json




      


set_tracing_disabled(disabled=True)
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_URL")

MODEL = "gemini-2.0-flash"

if not api_key or not base_url:
    raise ValueError("GEMINI_API_KEY and BASE_URL must be set in the environment variables.")

client = AsyncOpenAI(api_key=api_key, base_url=base_url)
model = OpenAIChatCompletionsModel(model=MODEL, openai_client=client)

@function_tool
def get_flights(destination: str, departure_time: str, days: int):
    """Returns flight options to a destination with user-specified departure time and number of travel days."""

    with open("flights.json", "r") as file:
        flights = json.load(file)
        result = []
        for flight in flights:
            if flight["destination"].lower() == destination.lower():
                result.append(f"{flight['flight_name']} {flight['id']} >>> {flight['destination']} at {departure_time} for {days} days")
    return "\n".join(result) if result else "No flights found for the specified destination."


@function_tool
def book_hotels(destination: str) -> str:
    """
    Returns available hotel rooms for a given destination.
    """
    with open("hotels.json", "r") as file:
        hotels = json.load(file)
        result = []
        for hotel in hotels:
            if hotel["destination"].lower() == destination.lower():
                result.append(f"Room {hotel['room_number']} (Hotel ID: {hotel['id']}) in {hotel['destination']}")

    return "\n".join(result) if result else "No hotel rooms found for the specified destination."


def travel_designer_agent(user_input: str, history: list):

    memory = "\n".join([f"User: {h['user']}\nAgent: {h['agent']}" for h in history])

    destination_agent = Agent(
    name="Destination Agent",
    instructions=f"""
You are a destination expert. Recommend travel destinations based on the user's interests and past inputs.

Conversation so far:
{memory}

Your tasks:
- Suggest destinations based on user preferences (e.g., relaxing, adventurous, cultural, nature).
- Mention a few popular attractions or highlights at each location.
- If user confirms a destination (e.g., "Okay, I’ll go to Bali"), suggest proceeding with flight/hotel booking and hand off to Booking Agent to book a flight/hotel for user.

""",
    model=model,
)


    booking_agent = Agent(
        name="Booking Agent",
        instructions=f"""
You are a booking agent. Your job is to help users book flights and hotels in a specific destination.
Previous conversation:
{memory}

Here are some examples of what you can do:
- If user selects a destination, you can help them book flights and hotels in that specific destination.
- You can provide information about available flights, hotels, and their prices.
- You can also assist users in making reservations and providing booking confirmations using get_flights tool and help user to book the flight.
- Once you have destination, departure_time, and days, call get_flights(destination, departure_time, days).
- When the user asks to book a hotel, call the book_hotels(destination) tool.
- After getting the result, pick the first available hotel, confirm the booking, and remember the room number.
- If the user later asks "room number" or "hotel details", recall what was booked and respond with it.


 
""",
        model=model,
        tools=[get_flights, book_hotels],
    )
    
    explore_agent = Agent(
    name="Explore Agent",
    instructions=f"""
You are an explore agent. Recommend attractions, food, and cultural experiences at a destination.

Use context from the conversation:
{memory}

Tasks:
- Suggest sightseeing spots, local experiences, or food recommendations.
- If user asks “What can I do in ___?” or mentions exploring, respond with relevant suggestions.
""",
    model=model,
)


    travel_agent = Agent(
        name="Travel Designer Agent",
        instructions=f"""
You are a travel designer agent. Your job is to help users plan trips step-by-step.

Use the following guidelines:
- If the user says something like "I want a relaxing trip" or "suggest places to hike", hand off to the Destination Agent.
- If the user says "Book a flight to Maldives", "Show flights for Bali", or "Book a hotel in Dubai", hand off to Booking Agent and call the relevant tool.
- If the user says "What can I do in Turkey?" or "Best food in Thailand?", hand off to Explore Agent.


Always guide the user through the next step after a response.
Previous conversation:
{memory}
""",
        model=model,
        handoffs=[destination_agent, booking_agent, explore_agent],
    )
    
    


    runner = Runner.run_sync(
        starting_agent=travel_agent,
        input=user_input,
    )

    print(f"\n🧭 Agent: {runner.final_output}\n")

    history.append({
        "user": user_input,
        "agent": runner.final_output
    })


def main():
    print("\n<---Greetings from Travel Designer Agent--->\n")
    conversation_history = []

    while True:
        try:
            user_input = input("\nEnter your query: ")
        except:
            print("Invalid Input!")
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("\nThank you for using Travel Designer Agent. Goodbye!\n")
            break

        travel_designer_agent(user_input, conversation_history)


if __name__ == "__main__":
    main()
