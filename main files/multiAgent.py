import asyncio
from autogen_agentchat.agents import (AssistantAgent)
from open_router import open_router
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.messages import TextMessage
import os 
from dotenv import load_dotenv
model_client = open_router

load_dotenv()
OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")


open_router_model_client =  OpenAIChatCompletionClient(
    base_url="https://openrouter.ai/api/v1",
    model= "deepseek/deepseek-r1-0528:free",
    api_key = OPEN_ROUTER_API_KEY,
    model_info={
        "family":"deepseek",
        "vision" :True,
        "function_calling":True,
        "json_output": False
    }
)


tools_fetcher = AssistantAgent(
    name = 'tools_fetcher',
    model_client=open_router_model_client,
    system_message="You are a best tools matcher suggest best tools for the given described query"
)

llm_fetcher = AssistantAgent(
    name = 'llms_fetcher',
    model_client=open_router_model_client,
    system_message="according to the query and teh suggested tools give me the best llm to develope the query"
)

clarifying_agent = AssistantAgent(
    name = 'clarifying_Agent',
    model_client=open_router_model_client,
    system_message="Ask any clarrifying questions and make sure the best tools are beeing suggested"
)


from autogen_agentchat.teams import RoundRobinGroupChat

team = RoundRobinGroupChat(
    participants= [clarifying_agent, tools_fetcher, llm_fetcher],
    max_turns=2
)




async def test_team():
    task = TextMessage(
        content='design a best animated website for a social media influencer',
        source='user'
    )

    result = await team.run(task=task)
    for each_agent_message in result.messages:
        print(f'{each_agent_message.source} : {each_agent_message.content}')

        
if __name__ == "__main__":
    asyncio.run(test_team())