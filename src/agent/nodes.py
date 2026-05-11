# Agent nodes
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, ToolMessage
from langgraph.prebuilt import ToolNode
from src.agent.state import AgentState
from src.agent.prompts import get_system_prompt
from src.tools import all_tools
from src.config import settings

from rich import print

llm = ChatGroq(
    api_key=settings.openai_api_key,
    model_name=settings.model_name,
    temperature=0.3,
)

llm_with_tools = llm.bind_tools(all_tools)

tool_node = ToolNode(all_tools)


async def agent_node(state: AgentState) -> dict:
    """Main agent node - calls LLM with tools."""
    system_prompt = get_system_prompt(
        user_id=state["user_id"],
        user_name=state["user_name"],
    )

    messages = [SystemMessage(content=system_prompt)] + state["messages"]
    response = await llm_with_tools.ainvoke(messages)

    return {"messages": [response]}


def should_continue(state: AgentState) -> str:
    """Route: if LLM called a tool -> tools node, else -> END."""
    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"
