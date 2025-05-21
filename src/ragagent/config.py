from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )
        # --- OPENAI Configuration ---
    OPENAI_API_KEY: str
    OPENAI_LLM_MODEL: str = "gpt-4o"
    OPENAI_LLM_MODEL_CONTEXT_SUMMARY: str = "gpt-4o-mini"
    
    # --- MongoDB Configuration ---
    MONGO_CONN_STR: str = "mongodb+srv://saurabhbhardwaj:saurabh27@ragagent.zegxhhs.mongodb.net/"
    
    MONGO_URI: str = Field(
        default = MONGO_CONN_STR,
        description ="Connection URI for the local MongoDB Atlas instance.",
    )
    
    MONGO_DB_NAME: str = "rag_agent"
    MONGO_STATE_CHECKPOINT_COLLECTION: str = "agent_state_checkpoints"
    MONGO_STATE_WRITES_COLLECTION: str = "agent_state_writes"
    MONGO_LONG_TERM_MEMORY_COLLECTION: str = "agent_long_term_memory"
    

    # --- Comet ML & Opik Configuration ---
    COMET_API_KEY: str | None = Field(
        default=None, description="API key for Comet ML and Opik services."
    )
    
    COMET_PROJECT: str = Field(
        default="rag_agent",
        description="Project name for Comet ML and Opik tracking.",
    )

    # --- Agents Configuration ---
    TOTAL_MESSAGES_SUMMARY_TRIGGER: int = 20
    TOTAL_MESSAGES_AFTER_SUMMARY: int = 8

    # --- RAG Configuration ---
    RAG_TEXT_EMBEDDING_MODEL_ID: str = "text-embedding-3-large"
    RAG_TEXT_EMBEDDING_MODEL_DIM: int = 3072
    RAG_TOP_K: int = 3
    RAG_DEVICE: str = "cpu"

    # --- Paths Configuration ---
    EVALUATION_DATASET_FILE_PATH: Path = Path("dataset\evaluation_dataset.json")
    RAGENT_DATA_DIR: str = "dataset/trainingdata.csv"


settings = Settings()