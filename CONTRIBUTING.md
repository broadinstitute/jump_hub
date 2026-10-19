# Contributing to JUMP Hub

## Quick Start

### Setup Development Environment

```bash
# Clone the repo
git clone https://github.com/broadinstitute/jump_hub.git
cd jump_hub

# Option 1: Use Nix (includes everything: Python, uv, Quarto)
nix develop --impure
# Type 'exit' to leave the Nix environment

# Option 2: Manual setup
uv sync --group dev
# Also install Quarto: https://quarto.org/docs/get-started/
```

### Make Changes

#### For Documentation (most common)
1. **Edit markdown files** in `explanations/`, `howto/`, or `reference/`
2. **Preview changes**: `quarto preview`
3. **Check rendering**: Navigate to your changed pages in the preview

#### For Code Tutorials
1. **Edit Python scripts** in `scripts/` (these use Jupytext percent format with `# %%` markers)
2. **Test your script runs**: `uv run python scripts/your_tutorial.py`
3. **Preview website**: `quarto preview` (Quarto can render .py files directly)

**Important**: DO NOT generate .ipynb files locally - they are created automatically during deployment

### Test tutorial execution without Nix or Quarto

From the repository root:

```bash
uv sync --locked --dev --python 3.11
uv run --locked python -m ipykernel install --sys-prefix --name python3
JUPYTER_PREFER_ENV_PATH=1 MPLBACKEND=Agg uv run --locked pytest tests/test_notebooks.py -v
```

To run one tutorial, add a selector such as `-k 13_calculate_activity`.
The tests read the Jupytext scripts into memory and execute each in a fresh
kernel and temporary working directory. They do not generate `.ipynb` files or
modify the tutorial sources. A failing cell fails the test; each cell has a
five-minute timeout. If UV-managed Python cannot locate your system's CA
certificates, set `SSL_CERT_FILE` to the system's trusted CA bundle; do not
disable TLS verification.

These are **integration tests**: they access public datasets and external APIs,
so network outages can cause failures. The GitHub Actions check runs on pull
requests and pushes to `main` that change scripts, dependencies, or the check
itself, and can also be started manually. It has a 30-minute job limit and
uploads a JUnit report for diagnosis. Documentation-only changes do not run it.

This check isolates notebook code and dependency failures from Nix, Quarto, and
publishing failures. The existing website workflow remains the end-to-end
rendering and deployment check.

## Deployment Process (Automated)

When changes are merged to `main`, GitHub Actions automatically:

1. **Converts Python scripts to notebooks**: Using Jupytext, all scripts in `scripts/` are converted to Jupyter notebooks
2. **Builds and publishes website**: Quarto renders all content and publishes to GitHub Pages (`gh-pages` branch)
3. **Creates Google Colab versions**: 
   - Notebooks from the built site are copied
   - A `!pip install jump_deps` cell is inserted at the beginning of each notebook
   - These are pushed to the `colab` branch for easy Google Colab access

This process is handled by:
- `.github/workflows/build_website.yml` - Triggers on push to main
- `tools/deploy.sh` - Orchestrates the conversion, build, and Colab generation
- `tools/insert_colab_cell.py` - Adds dependency installation to Colab notebooks
