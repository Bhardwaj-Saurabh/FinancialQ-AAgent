from pathlib import Path

from ragagent.application.data_ingestion.ingest import DataIngestion

def main() -> None:
    """CLI command to create long-term memory for philosophers.

    Args:
        metadata_file: Path to the philosophers extraction metadata JSON file.
    """
    data_ingestion = DataIngestion.build_from_settings()
    data_ingestion()


if __name__ == "__main__":
    main()