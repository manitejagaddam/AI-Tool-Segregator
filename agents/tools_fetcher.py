from autogen_agentchat.agents import AssistantAgent
from open_router import open_router


def tool_fetcher():
    tools_fetcher = AssistantAgent(
        name="tools_fetcher",
        model_client=open_router(),
        system_message="""
            You are an expert tool recommender for developers.
            Given a clarified query, suggest ONLY the most relevant tools or APIs that help solve the problem.
            Return output in this format:
            Recommended Tools:
            - Tool 1
            - Tool 2
            - Tool 3
            Do NOT explain or justify. Do NOT recommend LLMs. Only give tool names.
        """.strip()
    )
    
    return tools_fetcher