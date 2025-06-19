from pathlib import Path

import nbformat
from nbformat.notebooknode import from_dict
from nbformat.validator import normalize


def insert_deps_cell(filepath: Path, out_dir: Path):
    """
    Insert a cell to install dependencies in filepath and save a copy of
    the resultant notebook in out_dir.
    """
    name = filepath.name
    with open(filepath, "r") as f:
        nb = nbformat.read(f, as_version=4)

    # Create a new cell with some content
    new_cell = from_dict({
        "cell_type": "code",
        "execution_count": 0,
        "metadata": {},
        "outputs": [],
        "source": "!pip install jump_deps",
        "id": nb.cells[0]["id"][::-1],
    })
    # Append the new cell to the notebook's cells list
    nb.cells.insert(1, new_cell)

    _, nb2 = normalize(nb, version=nb["nbformat"], version_minor=nb["nbformat_minor"])
    # Save the modified notebook back to a file
    with open(out_dir / name, "w") as f:
        print(f"Writing {name}")
        nbformat.write(nb2, f, version=4)


if __name__ == "__main__":
    # Load the notebook from a file
    input_path = Path("howto/notebooks")
    colab_dir = Path("colab")
    colab_dir.mkdir(exist_ok=True, parents=True)

    files = list(input_path.glob("*.ipynb"))
    print(files)
    for fpath in files:
        insert_deps_cell(fpath, colab_dir)
