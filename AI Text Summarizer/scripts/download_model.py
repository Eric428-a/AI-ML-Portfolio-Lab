
### `scripts/download_model.py`

#python
from pathlib import Path


MODEL_DIRECTORY = Path("models")


def main() -> None:
    MODEL_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    print(
        "Model directory initialized:",
        MODEL_DIRECTORY.resolve(),
    )

    print(
        "Model downloading will be implemented "
        "when local inference is enabled."
    )


if __name__ == "__main__":
    main()