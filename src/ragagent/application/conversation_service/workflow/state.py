from langgraph.graph import MessagesState

class AgentState(MessagesState):
    """State class for the LangGraph workflow. It keeps track of the information necessary to maintain a coherent
    conversation between the agent and the user.
    """
    summary: str

def state_to_str(state: AgentState) -> str:
    if "summary" in state and bool(state["summary"]):
        conversation = state["summary"]
    elif "messages" in state and bool(state["messages"]):
        conversation = state["messages"]
    else:
        conversation = ""

    return f"""
            conversation={conversation})
            """