## Quirks and details

There are additional details that are not commonly asked but it is important to retain on record. This is a compendium of those.

- Source 1 and 9 use higher-density plates (1536 vs the standard 384\)  
- Genetic replicates were usually not randomized across well positions. Counting each ID's distinct `Metadata_Well` values in the [public metadata](https://github.com/jump-cellpainting/datasets/tree/main/metadata), approximately 99.4% of ORF IDs and 94.9% of CRISPR IDs occur at a single well coordinate across all plates on which they appear. Persistent position-specific effects could therefore contribute to apparent replicate consistency. This is a potential confound, not evidence that a phenotype is artifactual; controls, normalization, and the reuse of each coordinate by other reagents can help assess or reduce it.
- Source 7 and 13 are the same laboratory
- In JUMP-Target there is an InChIKey that maps to 2 different perturbations: ‘LOUPRKONTZGTKE-UHFFFAOYSA-N’ maps to both quinidine and quinine.  
- The definition of controls, especially positive controls, can be tricky: Some are hard-coded in [broad\_babel](https://github.com/broadinstitute/monorepo/blob/febe56c27e490c110d8b5a871de974a4293176c6/libs/jump_babel/tools/gen_database.py#L70-L87), based on internal knowledge that was not recorded at the time of assembling the datasets. In certain datasets, such as JUMP-ORF, there are additional types of positive controls: poscon\_orf, poscon\_cp (compound probe), and poscon\_diverse.
- The treatment compounds were assayed at 10 uM for all sources, except for
source_7 where the compounds were assayed at 0.625 uM (the goal being to assay some of the
compounds at a low concentration in addition to the higher concentration used for most of data
production). The positive control compounds in compound, ORF and CRISPR plates were assayed at 5
uM. JUMP-Target-1-Compound and JUMP-Target-2-Compound plates were also assayed at 5 uM
- Due to some plates having letters and numbers and others only numbers, be careful when loading multiple `load_data_csv`s. We treat all columns as strings to avoid any potential casting issue.
