from pathlib import Path


def evaluate() -> None:
    input_directory = Path("data/input")
    output_directory = Path("data/output")

    input_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    input_files = list(
        input_directory.glob("*")
    )

    print(
        f"Found {len(input_files)} input files."
    )

    print(
        "Evaluation pipeline is ready for "
        "model-quality metrics."
    )


if __name__ == "__main__":
    evaluate()