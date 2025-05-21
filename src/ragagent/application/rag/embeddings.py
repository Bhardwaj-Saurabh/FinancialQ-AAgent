from langchain_openai import OpenAIEmbeddings
from ragagent.config import settings

EmbeddingsModel = OpenAIEmbeddings

def get_embedding_model(
    model_id: str
) -> OpenAIEmbeddings:
    """Gets a OpenAIEmbeddings embedding model instance.

    Returns:
        OpenAIEmbeddings: A configured openai embeddings model instance
    """
    return OpenAIEmbeddings(
        model=model_id,
        api_key=settings.OPENAI_API_KEY,
    )