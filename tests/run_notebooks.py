"""Execute mandatory notebooks in order (no Papermill needed)."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = [
    "01_prepare_and_eda.ipynb",
    "02_time_split_and_baseline.ipynb",
    "03_regression_forecast.ipynb",
]
if __name__ == "__main__":
    import nbformat
    from nbclient import NotebookClient

    for name in NOTEBOOKS:
        file = ROOT / "notebooks" / name
        notebook = nbformat.read(file, as_version=4)
        print("Executing", name, flush=True)
        client = NotebookClient(notebook, timeout=240, kernel_name="python3",
                                resources={"metadata": {"path": str(ROOT)}})
        client.execute()
        print("PASS", name, flush=True)
    print("PASS: all three mandatory notebooks.")
