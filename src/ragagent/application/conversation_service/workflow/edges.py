from typing_extensions import Literal

from langgraph.graph import END

from ragagent.application.conversation_service.workflow.state import AgentState
from ragagent.config import settings


def should_summarize_conversation(
    state: AgentState,
) -> Literal["summarize_conversation_node", "__end__"]:
    messages = state["messages"]

    if len(messages) > settings.TOTAL_MESSAGES_SUMMARY_TRIGGER:
        return "summarize_conversation_node"

    return END