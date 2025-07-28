from autogen_agentchat.agents import AssistantAgent
from open_router import open_router

def clarifying_agent():
    clarifying_agent = AssistantAgent(
        name="clarifying_agent",
        model_client=open_router(),
        system_message="""
    You are a smart dev assistant.
    Your job is to ask up to 2 clarifying questions to refine the user's vague or broad query. Do NOT suggest tools or LLMs yet.
    Respond in this format:
    Clarifying Questions:
    1. <question 1>
    2. <question 2>
    """.strip()
    )
    
    return clarifying_agent