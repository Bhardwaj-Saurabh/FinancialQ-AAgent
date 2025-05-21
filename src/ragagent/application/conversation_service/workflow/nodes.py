from langchain_core.messages import RemoveMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import ToolNode

from ragagent.application.conversation_service.workflow.chains import (
    get_response_chain,
    get_conversation_summary_chain,
)
from ragagent.application.conversation_service.workflow.state import AgentState
from ragagent.application.conversation_service.workflow.tools import tools
from ragagent.config import settings

tool_node = ToolNode(tools)

async def conversation_node(state: AgentState, config: RunnableConfig):
    query = state.get("messages", "")[-1].content
    summary = state.get("summary", "")
    
    conversation_chain = get_response_chain()
    
    response = await conversation_chain.ainvoke(
        {"question": query,
         "summary": summary,
         "messages" : state["messages"],
        },
        config,
    )
    return {"messages": response}


async def summarize_conversation_node(state: AgentState):
    summary = state.get("summary", "")
    messages = state["messages"]

    if len(messages) > settings.TOTAL_MESSAGES_SUMMARY_TRIGGER:
        summary_chain = get_conversation_summary_chain(summary)

        response = await summary_chain.ainvoke(
            {
                "messages": state["messages"],
                "summary": summary,
            }
        )
        
        summary = response.content

        messages = [
            RemoveMessage(id=m.id)
            for m in state["messages"][: -settings.TOTAL_MESSAGES_AFTER_SUMMARY]
        ]
    
    return {"summary": summary, "messages": messages}