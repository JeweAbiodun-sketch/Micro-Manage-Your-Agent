import json
from pathlib import Path


NOTEBOOK = Path("blog_eval_langsmith.ipynb")


def sanitize_notebook(path: Path) -> None:
    nb = json.loads(path.read_text(encoding="utf-8"))

    cleaned_cells = []
    for cell in nb.get("cells", []):
        source = cell.get("source", "")
        if isinstance(source, list):
            source = "".join(source)

        cleaned = {
            "cell_type": cell.get("cell_type", "code"),
            "metadata": cell.get("metadata", {}) or {},
            "source": source,
        }

        if "id" in cell:
            cleaned["id"] = cell["id"]

        if cleaned["cell_type"] == "code":
            cleaned["execution_count"] = None
            cleaned["outputs"] = []

        cleaned_cells.append(cleaned)

    cleaned_nb = {
        "cells": cleaned_cells,
        "metadata": nb.get("metadata", {}) or {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    path.write_text(json.dumps(cleaned_nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sanitize_notebook(NOTEBOOK)
