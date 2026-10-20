# Example: protein localization with MisLocus

**Biological question:** does a protein variant change where the protein is
located in a cell?

[MisLocus](https://github.com/runxi-shen/MisLocus) is a related example of using
image-based representations to compare reference and variant proteins. It uses
single-cell images from **VarChAMP**, not the JUMP Cell Painting dataset.

## Start with precomputed features

The [public dataset](https://huggingface.co/datasets/anonymous-xyz96/MisLocus)
includes cleaned features from CellProfiler, Cytoself, MorphEm, and SubCell
variants, plus cell metadata and optional four-channel image crops. You can
reuse the features without running an image encoder.

1. Follow the repository's [feature-download instructions](https://github.com/runxi-shen/MisLocus#download-published-features)
   to select one representation and imaging batch rather than downloading the
   full dataset.
2. Follow the [CPU scoring guide](https://github.com/runxi-shen/MisLocus/blob/main/docs/dataset_bundle.md#run-cpu-scoring-on-published-features)
   to check cell identities and comparison cohorts, then compare variant cells
   with matched reference cells using classification or phenotypic-activity
   scores.
3. Use the [benchmark workflow](https://github.com/runxi-shen/MisLocus#benchmark-workflow)
   to evaluate scores against variant annotations or retrieve reference-protein
   localizations using Human Protein Atlas labels.

Published feature files are already cleaned: **do not normalize them again**.
Preserve the documented replicate splits and control calibration when comparing
representations. Detectable image differences alone do not establish a variant's
clinical pathogenicity.

This example runs in the companion repository's own environment; it is not one
of the Hub's Colab notebooks. Consult its maintained guides for installation,
dataset revisions, and analysis settings.
