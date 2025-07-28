import streamlit as st
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

# Agents
from agents.open_router import open_router
from agents.llm_fetcher import llm_fetcher
from agents.clarifying_Agent import clarifying_agent
from agents.tools_fetcher import tool_fetcher

# # Load keys
# load_dotenv()
# OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER_API_KEY")

# # Set up model client
# open_router_model_client = OpenAIChatCompletionClient(
#     base_url="https://openrouter.ai/api/v1",
#     model="deepseek/deepseek-r1-0528:free",
#     api_key=OPEN_ROUTER_API_KEY,
#     model_info={
#         "family": "deepseek",
#         "vision": True,
#         "function_calling": True,
#         "json_output": False
#     }
# )

# # Define Agents
# tools_fetcher = AssistantAgent(
#     name="tools_fetcher",
#     model_client=open_router_model_client,
#     system_message="""
# You are an expert tool recommender for developers.
# Given a clarified query, suggest ONLY the most relevant tools or APIs that help solve the problem.
# Return output in this format:
# Recommended Tools:
# - Tool 1
# - Tool 2
# - Tool 3
# Do NOT explain or justify. Do NOT recommend LLMs. Only give tool names.
# """.strip()
# )

# llm_fetcher = AssistantAgent(
#     name="llm_fetcher",
#     model_client=open_router_model_client,
#     system_message="""
# You are an expert LLM selector.
# Given the clarified query and tool list, suggest only the best LLMs or models suited for the task.
# Output format:
# Recommended LLMs:
# - LLM 1
# - LLM 2
# Do NOT explain or add descriptions. Just model names.
# """.strip()
# )

# clarifying_agent = AssistantAgent(
#     name="clarifying_agent",
#     model_client=open_router_model_client,
#     system_message="""
# You are a smart dev assistant.
# Your job is to ask up to 2 clarifying questions to refine the user's vague or broad query. Do NOT suggest tools or LLMs yet.
# Respond in this format:
# Clarifying Questions:
# 1. <question 1>
# 2. <question 2>
# """.strip()
# )

# Team Chat
team = RoundRobinGroupChat(
    participants=[tool_fetcher(), llm_fetcher(), clarifying_agent()],
    max_turns=3
)


# Async team runner
async def run_team(user_input):
    task = TextMessage(content=user_input, source='user')
    result = await team.run(task=task)
    return result.messages




# Streamlit UI
st.set_page_config(page_title="AI Tool + LLM Recommender", layout="centered")
st.title("🔧 LLM & Tool Suggestion Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Enter your project idea...", placeholder="e.g. I want to build a fitness tracking app")

if st.button("Submit") and user_input:
    st.session_state.chat_history.append(("User", user_input))

    with st.spinner("Let the agents brainstorm..."):
        messages = asyncio.run(run_team(user_input))

    for msg in messages:
        st.session_state.chat_history.append((msg.source, msg.content))

# Display chat history
for sender, content in st.session_state.chat_history:
    if sender.lower() == "user":
        st.chat_message("user").write(content)
    else:
        st.chat_message("assistant").write(f"**{sender.upper()}**:\n{content}")
