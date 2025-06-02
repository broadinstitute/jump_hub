# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

JUMP Hub is a documentation and tutorial website for the JUMP Cell Painting project. It serves as the central resource for accessing and analyzing large-scale morphological profiling datasets used in biological research.

## Development Environment Setup

### Using Nix (Recommended)
```bash
nix develop --impure
```
This automatically sets up Python 3.11, uv, Quarto, and all development tools. Exit with `exit` when done.

### Using uv Directly
```bash
uv sync --group dev
```

## Common Development Commands

### Testing Tutorial Scripts
```bash
# Test a tutorial script runs without errors
uv run python scripts/11_retrieve_profiles.py
```

## Architecture

### Content Pipeline
1. **Tutorial scripts** are written as Python files in `scripts/` using Jupytext percent format
2. **Jupytext** automatically converts these to Jupyter notebooks 
3. **Quarto** renders notebooks into website documentation

### Key Directories
- `scripts/` - Main tutorial content as executable Python scripts
- `howto/` - Quarto markdown documentation and guides  
- `explanations/` - Background information and dataset descriptions
- `reference/` - Technical reference materials and utilities
- `workspace/analysis/` - Research examples and work-in-progress analyses
- `tools/` - Build and deployment utilities

### Python Package Structure
The repository doubles as a Python package (`jump_deps`) that provides all necessary dependencies for JUMP data analysis. The package is a convenience wrapper that installs:
- Data processing libraries (polars, pyarrow, boto3)
- Visualization tools (matplotlib, seaborn) 
- Biology-specific packages (biopython, broad-babel)
- JUMP ecosystem tools (jump-portrait, copairs)

## Content Creation Workflow

1. Write tutorials as Python scripts in `scripts/` using `# %%` cell markers
2. Test notebooks work correctly with JUMP data
3. Run `quarto preview` to preview website locally

## Important Notes

- Python scripts in `scripts/` are the source of truth - edit these, not the generated notebooks
- The `colab` branch contains Google Colab-compatible versions with dependency installation cells
- Website is published to GitHub Pages via the `gh-pages` branch
- Dependencies are constrained to Python 3.10-3.11 for compatibility with JUMP ecosystem