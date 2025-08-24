from utils import openai_client

def agregate_research(topic: str, content: str):
    SYSTEM_PROMPT = """
        You are a research synthesis expert who creates comprehensive, well-structured reports from multiple sources.

        # YOUR TASK
        Analyze the provided research content and create a thorough summary that synthesizes information across all sources into a coherent, insightful report.

        # SYNTHESIS REQUIREMENTS
        - **Integrate information** from all sources rather than simply listing findings
        - **Identify patterns, trends, and relationships** across different sources
        - **Highlight key insights** and major themes that emerge from the research
        - **Note contradictions or differing perspectives** when they exist
        - **Organize content logically** with clear sections and flow

        # REPORT STRUCTURE
        1. **Executive Summary** - Key findings and main conclusions (2-3 paragraphs)
        2. **Main Content** - Detailed analysis organized by themes/topics
        3. **Key Insights** - Important patterns or discoveries from the research
        4. **Considerations** - Limitations, contradictions, or areas needing further research

        # QUALITY STANDARDS
        - Write in clear, professional prose
        - Support claims with evidence from the sources
        - Maintain objectivity while drawing meaningful conclusions
        - Ensure the report is comprehensive yet focused
        - Make it actionable and valuable for decision-making
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
                "content": f"Topic: {topic}.\nContent after research: {content}",
            },
        ]
    )
    
    with open(f"{topic}.md", "w") as f:
        f.write(res.choices[0].message.content)

    return f"Research content for topic '{topic}' has been aggregated and saved to {topic}.md"


agregate_research_def = {
    "type": "function",
    "function": {
        "name": "agregate_research",
        "description": "Create a comprehensive summary of the research content based on the provided topic and content.",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "The topic of the research.",
                },
                "content": {
                    "type": "string",
                    "description": "The content after research.",
                },
            },
            "required": ["topic", "content"],
        },
    },  
}