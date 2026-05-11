# LangGraph agent graph
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from src.agent.state import AgentState
from src.agent.nodes import agent_node, tool_node, should_continue


def build_graph():
    """Build and compile the LangGraph agent."""
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("agent", agent_node)
    graph.add_node("tools", tool_node)

    # Entry point
    graph.set_entry_point("agent")

    # Conditional routing
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END,
        },
    )

    # After tools, always to back to agent
    graph.add_edge("tools", "agent")

    # MemorySaver gives per-thread (per-user) conversation memory
    memory = MemorySaver()
    return graph.compile(checkpointer=memory)


# Singleton compiled graph
appointment_graph = build_graph()
