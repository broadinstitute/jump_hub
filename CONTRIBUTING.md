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
