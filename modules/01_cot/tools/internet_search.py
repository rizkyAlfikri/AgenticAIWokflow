import json
from utils import tavily_client
from utils import openai_client

def internet_search(query: str):
    SYSTEM_PROMPT = """
        You are an information extraction specialist who identifies and extracts key facts from web search results and documents.

        # YOUR TASK
        Extract the most important and relevant information from the provided text, organizing it into clear, concise bullet points.

        # EXTRACTION CRITERIA
        - Focus on **factual information** - data, statistics, findings, claims, and concrete details
        - Prioritize **unique insights** and information not commonly known
        - Include **specific details** like numbers, dates, names, and locations when present
        - Capture **different perspectives** or viewpoints mentioned in the text
        - Extract **actionable information** and practical insights

        # FORMATTING REQUIREMENTS
        - One key point per bullet
        - Keep bullets concise but complete (1-2 sentences maximum)
        - Start each bullet with the most important information
        - Maintain original meaning and context
        - Preserve specific data, quotes, and technical terms

        # QUALITY STANDARDS
        - Extract 5-10 key points depending on content richness
        - Avoid redundant or overly similar points
        - Skip generic statements or widely known information
        - Ensure each bullet adds unique value to understanding the topic
        """

    res = tavily_client.search(query, include_raw_content="markdown", max_results=3)
    results = res.get("results")

    res = openai_client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": json.dumps(results),
            },
        ]
    )
    return res.choices[0].message.content
    
internet_search_def = {
    "type": "function",
    "function": {
        "name": "internet_search",
        "description": "Search the internet for a given query", "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to perform.",
                },
            },
            "required": ["query"],
        },
    },  
}