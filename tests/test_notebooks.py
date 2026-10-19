"""Check that tutorial notebooks run with the declared Python dependencies."""

from pathlib import Path

import jupytext
import pytest
from nbclient import NotebookClient

SCRIPTS = sorted((Path(__file__).resolve().parents[1] / "scripts").glob("*.py"))
assert SCRIPTS, "No tutorial scripts found"


@pytest.mark.integration
@pytest.mark.parametrize("script", SCRIPTS, ids=lambda script: script.name)
def test_notebook_execution(script, tmp_path, monkeypatch):
    # Do not inherit local IPython startup scripts or Jupyter configuration.
    monkeypatch.setenv("IPYTHONDIR", str(tmp_path / "ipython"))
    monkeypatch.setenv("JUPYTER_CONFIG_DIR", str(tmp_path / "jupyter"))
    notebook = jupytext.read(script)
    assert any(cell.cell_type == "code" and cell.source.strip() for cell in notebook.cells)

    # Each tutorial gets a fresh kernel and working directory. Read the percent
    # script into memory rather than syncing Jupytext's paired .qmd/.ipynb files.
    NotebookClient(
        notebook,
        kernel_name="python3",
        timeout=300,
        startup_timeout=60,
        allow_errors=False,
        resources={"metadata": {"path": str(tmp_path)}},
    ).execute()
