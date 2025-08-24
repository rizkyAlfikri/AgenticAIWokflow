from utils import openai_client

def research_plan(topic: str):
    SYSTEM_PROMPT = """
        You are a research planning expert who creates strategic search queries for comprehensive topic investigation.

        # YOUR TASK
        Generate 3-5 targeted search queries that will systematically cover different aspects of the given research topic.

        # QUERY DESIGN PRINCIPLES
        - Make each query specific and searchable (2-6 words typically work best)
        - Cover different angles: foundational concepts, recent developments, practical applications, expert opinions
        - Avoid overly broad terms that would return generic results
        - Include specific terminology, names, or technical terms when relevant
        - Consider temporal aspects (current trends, historical context, future projections)

        # OUTPUT FORMAT
        Return only the queries, one per line, without numbering or additional text.

        # EXAMPLE
        Topic: "Impact of remote work on productivity"
        - remote work productivity statistics 2025
        - hybrid work models employee performance
        - remote work challenges solutions
        - distributed team management best practices
        - future of work trends post-pandemic
        """

    res = openai_client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"Create a research plan for {topic}."
            },
        ],
    )
    return res.choices[0].message.content

research_plan_def = {
    "type": "function",
    "function": {
        "name": "research_plan",
        "description": "Create a detailed research plan for a given topic.",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The topic for which to create a research plan.",
                },
            },
            "required": ["topic"],
        },
    },  
}