import json

from loguru import logger
from tools.broadcast import broadcast, broadcast_def
from tools.research_agreator import agregate_research, agregate_research_def
from tools.research_plan import research_plan, research_plan_def
from tools.internet_search import internet_search, internet_search_def
from tools.translate import multiple_language_translate, multiple_language_translate_def
from utils import openai_client

tools: list = [
    broadcast_def,
    agregate_research_def,
    research_plan_def,
    internet_search_def,
    multiple_language_translate_def
]

def excute_function(function_name: str, function_args):
    if function_name == "broadcast":
        return broadcast(**function_args)
    elif function_name == "agregate_research":
        return agregate_research(**function_args)
    elif function_name == "research_plan":
        return research_plan(**function_args)
    elif function_name == "internet_search":
        return internet_search(**function_args)
    elif function_name == "multiple_language_translate_def":
        return multiple_language_translate(**function_args)
    else:
        return { "error": "Function not found"}
    

def process_research(topic: str): 
    SYSTEM_PROMPT = """
        You are an AI Research Assistant that conducts comprehensive research and delivers results in multiple languages.

        # YOUR MISSION
        Research any given topic thoroughly and deliver a complete research report in English, Indonesian, Japanese, and Korean.

        # RESEARCH PROCESS
        1. **Plan Research Strategy** - Create targeted search queries for comprehensive coverage
        2. **Execute Internet Research** - Gather information from multiple reliable sources  
        3. **Synthesize Findings** - Combine research into a comprehensive, well-structured report
        4. **Deliver Multilingual Results** - Translate final report to Indonesian, Japanese, and Korean

        # EXECUTION STANDARDS
        - **Always use available tools** - Never attempt tasks manually that tools can handle
        - **Provide clear progress updates** - Announce each step as you begin it
        - **Maintain research quality** - Focus on credible sources and accurate information
        - **Ensure completeness** - Cover all aspects of the topic systematically

        # COMMUNICATION PROTOCOL
        Before each major step, announce your progress:
        - "🔍 **PLANNING**: Creating research strategy for [topic]..."
        - "🌐 **RESEARCHING**: Gathering information from web sources..."  
        - "📊 **SYNTHESIZING**: Analyzing and combining research findings..."
        - "🌏 **TRANSLATING**: Preparing multilingual versions..."
        - "✅ **COMPLETE**: Research delivered in all requested languages"

        # SUCCESS CRITERIA
        - Comprehensive topic coverage using systematic research approach
        - Professional-quality report suitable for decision-making
        - Accurate translations that preserve meaning and technical terms
        - Clear documentation of research progress throughout process
        """

    print(f"Topic app: {topic}")
    messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Topic: {topic}."}
        ]

    while True:
        print(f"Messages app: {messages}")
        response = openai_client.chat.completions.create(
            model="gpt-4.1",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                logger.info(f"Executing tool: {function_name} with args: {function_args}");

                result = excute_function(function_name, function_args)
                
                messages.append({
                    "role": "tool",
                    "content": result,
                    "tool_call_id": tool_call.id,
                })
        else:
            break

    return "Research completed successfully."

if __name__ == "__main__":
    topic = "what's Experience Mobile Developer portgolio to getting a job at fintech company. The portolio must be simple, not complex and have a project that is related to AI and fintech company. Give 10 example project"
    process_research(topic)
