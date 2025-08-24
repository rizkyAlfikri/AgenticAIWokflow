from dotenv import load_dotenv
from openai import OpenAI
from tavily import TavilyClient

load_dotenv()

openai_client = OpenAI()
tavily_client = TavilyClient()