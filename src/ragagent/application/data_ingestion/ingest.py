from langchain_core.documents import Document
from loguru import logger

from ragagent.application.data_ingestion import extract_data_from_dataframe
from ragagent.application.rag.retrievers import Retriever, get_retriever
from ragagent.config import settings
from ragagent.infra.mongodb import MongoClientWrapper, MongoIndex


class DataIngestion:
    def __init__(self, retriever: Retriever) -> None:
        self.retriever = retriever

    @classmethod
    def build_from_settings(cls) -> "DataIngestion":
        retriever = get_retriever(
            embedding_model_id=settings.RAG_TEXT_EMBEDDING_MODEL_ID,
            k=settings.RAG_TOP_K
        )

        return cls(retriever)

    def __call__(self) -> None:

        # First clear the long term memory collection to avoid duplicates.
        with MongoClientWrapper(
            model=Document, collection_name=settings.MONGO_LONG_TERM_MEMORY_COLLECTION
        ) as client:
            client.clear_collection()

        documents = extract_data_from_dataframe(settings.RAGENT_DATA_DIR)
        # for i, docs in enumerate(documents):
        # logger.debug(f"Ingesting {i}th documents from Documents")
        self.retriever.vectorstore.add_documents(documents)

        self.__create_index()

    def __create_index(self) -> None:
        with MongoClientWrapper(
            model=Document, collection_name=settings.MONGO_LONG_TERM_MEMORY_COLLECTION
        ) as client:
            self.index = MongoIndex(
                retriever=self.retriever,
                mongodb_client=client,
            )
            self.index.create(
                is_hybrid=True, embedding_dim=settings.RAG_TEXT_EMBEDDING_MODEL_DIM
            )

class DataRetriever:
    def __init__(self, retriever: Retriever) -> None:
        self.retriever = retriever

    @classmethod
    def build_from_settings(cls) -> "DataRetriever":
        retriever = get_retriever(
            embedding_model_id=settings.RAG_TEXT_EMBEDDING_MODEL_ID,
            k=settings.RAG_TOP_K
        )

        return cls(retriever)

    def __call__(self, query: str) -> list[Document]:
        return self.retriever.invoke(query)