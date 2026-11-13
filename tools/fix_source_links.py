"""Quarto post-render hook: point "View/Edit source" links at the real sources.

Notebook pages are rendered from .qmd files that jupytext generates at build
time (scripts/*.py -> howto/notebooks/*.qmd, reference/00_gene_index.py ->
reference/00_gene_index.qmd). Those .qmd files are not committed, so Quarto's
repo-actions links 404. Rewrite them to the committed .py sources.
"""

import os
import re
import sys
from pathlib import Path

PATTERNS = [
    (re.compile(r"/(blob|edit)/main/howto/notebooks/([\w-]+)\.qmd"), r"/\1/main/scripts/\2.py"),
    (re.compile(r"/(blob|edit)/main/reference/00_gene_index\.qmd"), r"/\1/main/reference/00_gene_index.py"),
]


def main(out_dir: Path) -> None:
    for html in out_dir.rglob("*.html"):
        text = html.read_text(encoding="utf-8")
        new = text
        for pat, repl in PATTERNS:
            new = pat.sub(repl, new)
        if new != text:
            html.write_text(new, encoding="utf-8")
            print(f"fix_source_links: {html.relative_to(out_dir)}")


if __name__ == "__main__":
    main(Path(sys.argv[1] if len(sys.argv) > 1 else os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "docs")))
