# Glossary and Acronyms

Reference for terms and their definition.

- **Image-based profiling** (also called morphological profiling): Method to study cell phenotypes by quantifying their shape, size and intensity features. The many features that are captured make up the profile of the cell or the population of cells in a sample.  
- **Phenotypic activity**: Metric that indicates how well we can distinguish a perturbation from its negative controls, which quantifies how strong the phenotype is ([Kalinin, et al. elaborates on the term](https://doi.org/10.1038/s41467-025-60306-2)).  
- **Phenotypic consistency**: Metric that indicates how well a perturbation’s profile  matches profiles of samples that are expected to be biologically related, according to an annotated resource (e.g., known gene-gene or compound-target interactions ([Kalinin, et al.](https://doi.org/10.1038/s41467-025-60306-2)).  
- **Phenotypic distinctiveness**: Metric showing how distinctive a perturbation is relative to the other perturbations in a given experiment (not limited to negative controls, as in phenotypic activity).  
- **Cosine similarity**: Metric capturing how close two vectors are. It assumes all the elements in them (usually features) have the same weight.  
- **Retrievability:** Umbrella term for the methods that assess the quality of matching among a set of samples in a profiling experiment: **phenotypic activity**, **consistency**, and **distinctiveness**.  
- **Consensus profile**: Aggregated profiles across all biological replicates (e.g., across all wells) of a given perturbation, generally it is the median of every feature.

## Acronyms

- **JUMP**: Joint Undertaking for Morphological Profiling  
- **mAP**: mean Average Precision ([Kalinin, et al.](https://doi.org/10.1038/s41467-025-60306-2) explains mAP in the context of image-based profiling)  
- **CRISPR**: Clustered Regularly Interspaced Short Palindromic Repeats. This method was used to produce the CRISPR datasets, in which genes were knocked out.  
- **ORF**: Open Reading Frame. This method was used to produce the ORF datasets, in which genes were overexpressed.

## Other definitions

These definitions are related to [cytomining](https://github.com/cytomining) libraries and may not be relevant to the more recent tools. They are kept here in case you encounter them in papers/metadata.

- **poscon\_diverse**: Non-primary positive controls, this is experiment-specific.  
- **poscon\_cp**: Standard positive control used for compound studies (cp stands for compound probes).  
- **q-value: Expected False Discovery Rate (FDR)**: the proportion of false positives among all positive results.

