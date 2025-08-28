import json
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from loguru import logger


load_dotenv()

chroma_client = chromadb.PersistentClient(path="data")
ef = OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_API_KEY"), model_name="text-embedding-3-small")
collection = chroma_client.get_collection(name="companies_data", embedding_function=ef)


@function_tool
def query_collection(query_text: str, n_results: int = 5) -> str:
    """Get context from vector database for relevant information"""
    logger.info(f"Querying collection with query_text: {query_text} and n_results: {n_results}")
    result = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    return json.dumps(result.get("documents")[0])


SYSTEM_PROMPT = """
    You are assistant agent for answering questions about companies.

    RULES:
    - Always use query_collection to get relevant data based on user query
    - If there is no relevant data, then reply with "I don't know"
    - If there is relevant data, then use it to answer the question
    """

assistant_agent = Agent(
    name="Assistant Agent",
    instructions=SYSTEM_PROMPT,
    model="gpt-4.1",
    tools=[query_collection],
)

async def main():
    messages = []

    while True:
        user_input = input("User: ")
        messages.append({"role": "user", "content": user_input})
        runner = await Runner.run(starting_agent=assistant_agent, input=messages)
        messages = runner.to_input_list()

        print(runner.last_agent.name)
        print(runner.final_output)
        print("===" * 20)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())