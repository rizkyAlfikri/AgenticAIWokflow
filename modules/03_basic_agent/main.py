from agents import Agent, Runner, function_tool
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

@function_tool
def get_weather(city: str) -> str:
    """Fetches the current weather for a given city."""
    # Simulated weather data for demonstration purposes
    weather_data = {
        "New York": "Sunny, 25°C",
        "Los Angeles": "Cloudy, 22°C",
        "Chicago": "Rainy, 18°C",
        "Houston": "Sunny, 30°C",
        "Phoenix": "Hot, 35°C"
    }
    return weather_data.get(city, "Sunny, 20°C")

emojis_agest = Agent(
    name="Emojis Agent",
    instructions="You are fun assistant, with sense of humor. You respond to user queries with a funny message and relevant emojis.",
    model="gpt-4.1",
)

haiku_agent = Agent(
    name="Haiku Agent",
    instructions="You are a poetic assistant. You respond to user queries with a haiku poem",
    model="gpt-4.1",
    tools=[get_weather],
)

triage_agent = Agent(
    name="Triage Agent",
       instructions="""
        You are Triage Agent, that decide to handsoff the conversation based on user query.

        # RULES :
        - If user asking to talk to emojis agent, then hands off the conversation to Emojis Agent.
        - if user asking about fun activity, then hands off the conversation to Emojis Agent.

        - If user asking to talk to haiku agent, then hands off the conversation to Haiku Agent.
        - if user asking about haiku, then hands off the conversation to Haiku Agent.
        - if user asking about weather, then hands off the conversation to Haiku Agent.
        """,
        model="gpt-4.1",
        handoffs=[haiku_agent, emojis_agest], # List of agents to which this agent can hand off conversations
)

async def main():
    messages = []

    while True:
        user_query = input("User: ")
        messages.append({"role": "user", "content": user_query})
        runner = await Runner.run(starting_agent=triage_agent, input=user_query)
        messages = runner.to_input_list()

        print("\n--- Conversation so far ---")
        print(runner.last_agent.name)
        print(runner.final_output)
        print("---------------------------\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 
    