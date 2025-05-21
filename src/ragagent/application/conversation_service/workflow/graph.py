from functools import lru_cache

from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import tools_condition, ToolNode

from ragagent.application.conversation_service.workflow.edges import (
    should_summarize_conversation,
)

from ragagent.application.conversation_service.workflow.nodes import (
    conversation_node,
    summarize_conversation_node,
)
from ragagent.application.conversation_service.workflow.tools import tools
from ragagent.application.conversation_service.workflow.state import AgentState


@lru_cache(maxsize=1)
def create_workflow_graph():
    graph_builder = StateGraph(AgentState)

    # Define the flow
    graph_builder.add_node("conversation_node", conversation_node)
    graph_builder.add_node("summarize_conversation_node", summarize_conversation_node)
    graph_builder.add_node("tools", ToolNode(tools=tools))
    
    
    graph_builder.add_edge(START, "conversation_node")
    graph_builder.add_conditional_edges(
        "conversation_node",
        tools_condition,
        ["tools", END]
    )
    graph_builder.add_edge("tools", "conversation_node")
    graph_builder.add_conditional_edges("conversation_node", should_summarize_conversation)
    graph_builder.add_edge("summarize_conversation_node", END)
    
    return graph_builder

# Compiled without a checkpointer. Used for LangGraph Studio
graph = create_workflow_graph().compile()