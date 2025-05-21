from pathlib import Path

from ragagent.application.evaluation.evaluate import evaluate_agent
from ragagent.application.evaluation.upload_data import upload_dataset
from ragagent.config import settings

def main(name: str, data_path: Path, workers: int, nb_samples: int) -> None:
    """
    Evaluate an agent on a dataset.

    Args:
        name: Name of the dataset
        data_path: Path to the dataset file
        workers: Number of workers to use for evaluation
        nb_samples: Number of samples to evaluate
    """

    dataset = upload_dataset(name=name, data_path=data_path)
    evaluate_agent(dataset, workers=workers, nb_samples=nb_samples)


if __name__ == "__main__":
    name = "RagAgent_Evaluation"
    data_path = settings.EVALUATION_DATASET_FILE_PATH
    main(name, data_path, workers=1, nb_samples=5)