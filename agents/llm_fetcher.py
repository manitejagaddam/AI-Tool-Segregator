from autogen_agentchat.agents import AssistantAgent
from open_router import open_router


def llm_fetcher():
    llm_fetcher = AssistantAgent(
        name="llm_fetcher",
        model_client=open_router(),
        system_message="""
    You are an expert LLM selector.
    Given the clarified query and tool list, suggest only the best LLMs or models suited for the task.
    Output format:
    Recommended LLMs:
    - LLM 1
    - LLM 2
    Do NOT explain or add descriptions. Just model names.
    """.strip()
    )
    
    return llm_fetcher