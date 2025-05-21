
from langchain_openai import ChatOpenAI
from ragagent.config import settings

def get_chat_model(temperature: float = 0.1, model_name: str = settings.OPENAI_LLM_MODEL) -> ChatOpenAI:
    return ChatOpenAI(
        api_key=settings.OPENAI_API_KEY,
        model_name=model_name,
        temperature=temperature,
    )
