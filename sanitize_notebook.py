import json
from pathlib import Path


NOTEBOOK = Path("blog_eval_langsmith.ipynb")


def sanitize_notebook(path: Path) -> None:
    nb = json.loads(path.read_text(encoding="utf-8"))

    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            cell["outputs"] = []
            cell["execution_count"] = None

    path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sanitize_notebook(NOTEBOOK)
