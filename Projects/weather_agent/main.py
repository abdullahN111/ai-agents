import asyncio
import requests

import streamlit as st
from agents import Agent, Runner, function_tool

from config import model, weather_api_key, weather_base_url
from cities import cities

st.set_page_config(page_title="Super Weather", page_icon="☁️")
st.title("Check Super Weather")



@function_tool
def get_weather(city: str) -> str:
    url = f"{weather_base_url}?key={weather_api_key}&q={city}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        city_name = data["location"]["name"]
        temperature = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]

        return f"The temperature in {city_name} is {temperature}°C with {condition}."


    except requests.exceptions.RequestException as e:
        return f"Failed to fetch weather data: {e}"
    except KeyError:
        return "Weather data format error. Please check the city name."
        
    

async def main():
    weather_agent = Agent(name="Weather Agent", instructions="""
                          You are a weather agent, you will answer weather related queries for user.
                          Here is what you will do:
                          - Answer queries about weather conditions in past all around the world.
                          - Answer queries about the affects of climate change on world.
                          - Tell realtime weather data using get_weather tool.
                          
                          Note: Do not answer anything else beyond your instructions. and keep the response in short paragraphs.
                          """,
                          model=model,
                          tools=[get_weather],
                          )
    
    try:
       
        city_list = st.selectbox("Cities", cities)
        if st.button("Check Weather"):
            runner = await Runner.run(weather_agent, city_list)
            st.success(runner.final_output)

        
        user_input = st.text_input("Say something")
        if st.button("Ask Something"):
           
            runner = await Runner.run(weather_agent, user_input)
            st.success(runner.final_output)

    except Exception as e:
        st.warning(f"Something went wrong: {e}")
        

    
    
if __name__ == "__main__":
    asyncio.run(main())