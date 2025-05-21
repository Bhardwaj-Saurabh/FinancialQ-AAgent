from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


from ragagent.application.conversation_service.workflow.tools import tools
from ragagent.config import settings
from ragagent.domain.prompts import (
    CONVERSATION_PROMPT,
    DOCUMENT_GRADER_PROMPT,
    EXTEND_SUMMARY_PROMPT,
    SUMMARY_PROMPT,
)

from ragagent.application.conversation_service.workflow.chat_model import get_chat_model

from operator import itemgetter


def get_response_chain():
    model = get_chat_model()
    model = model.bind_tools(tools)
    system_message = CONVERSATION_PROMPT

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system",system_message.prompt),
             MessagesPlaceholder(variable_name="messages"),
        ],
        template_format="jinja2",
        )
    
    qa_rag_chain = prompt | model

    return qa_rag_chain

def get_conversation_summary_chain(summary: str = ""):
    model = get_chat_model(model_name=settings.OPENAI_LLM_MODEL_CONTEXT_SUMMARY)

    summary_message = EXTEND_SUMMARY_PROMPT if summary else SUMMARY_PROMPT

    prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="messages"),
            ("human", summary_message.prompt),
        ],
        template_format="jinja2",
    )

    return prompt | model