#/usr/bin/env bash
# Script that converts python scripts into notebooks, runs and publishes them to a website using Quarto and
# generates a notebook in another branch that mimics the original one, but adds a cell containing '!pip install jump_deps'
jupytext --sync scripts/*.py &&
	jupytext --to qmd reference/00_gene_index.py &&
	git config --global user.email quarto-github-actions-publish@example.com &&
	git config --global user.name Quarto_GHA_Runner &&
	export QUARTO_PYTHON=$(which python) &&
	quarto publish gh-pages &&
	echo "Generating collab files" &&
	git status &&
	git restore --source gh-pages -- "howto/notebooks/*.ipynb" &&
	ls howto &&
	python tools/insert_colab_cell.py &&
	ls colab &&
	git add colab/* && git commit -m 'add colab files' && git push --force origin main:colab
