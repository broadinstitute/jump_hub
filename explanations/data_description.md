# Dataset Overview

## Dataset Collection

This collection comprises 4 datasets:

- Principal dataset (`cpg0016`): 116k chemical and \~22k gene perturbations, split across 12 data-generating centers using human U2OS osteosarcoma cells. This includes JUMP-ORF, JUMP-CRISPR, and JUMP-compounds  
- 3 pilot datasets testing:  
  - Different perturbation conditions (`cpg0000-jump-pilot`, including different cell types)  
  - Staining conditions (`cpg0001-cellpainting-protocol`)  
  - Microscopes (`cpg0002-jump-scope`)

## Design of the Dataset

### Cell Line Selection

- We chose U2OS (osteosarcoma) cells for our major data production work because phenotypes are equally or more visible than the few other lines we’ve tested and there is existing data in this cell type (namely, cpg0012-wawer-bioactivecompoundprofiling)

### Perturbation Types in cpg0016

- **Genetic Perturbations:**  
  - CRISPR knockdowns of \~8k genes (pooled guides targeting each gene are arrayed into plates)  
  - ORF (overexpression) reagents for \~12k unique genes, with \~5k that overlap with CRISPR targets
 
  Do note that these numbers were based on JUMP Cell Painting IDs and there may be some minor duplication of genes.
  
- **Chemical Perturbations:**  
  - Partners exchanged \~115,795 compounds  
  - \~5 replicates of each compound  
  - Performed as 1-2 replicates at 3-5 different sites globally  
    

### Control Sets of genes and compounds

- **JUMP-Target:**  
    
  - 306 compounds and 160 corresponding genetic perturbations  
  - Designed to assess connectivity (gene-compound matching, based on annotated gene targets of each compound) in profiling assays  
  - Includes 384-well plate maps  
  - [Documentation](https://github.com/jump-cellpainting/JUMP-Target)


- **JUMP-MOA:**  
    
  - 90 compounds in quadruplicate, laid out on a 384-well plate  
  - Represents 47 mechanism-of-action classes  
  - Designed for assessing connectivity between genes and compounds  
  - [Documentation](https://github.com/jump-cellpainting/JUMP-MOA)


- **Positive Controls:**  
    
  - Set of 8 compounds per sample plate  
  - [List of recommended controls](https://github.com/jump-cellpainting/JUMP-Target#positive-control-compounds)

### Cell Painting Protocol

The experiments used an optimized Cell Painting protocol, published in [Cimini et al. Nature Protocols 2023](https://pubmed.ncbi.nlm.nih.gov/37344608/), which builds upon the original [Bray et al. Nature Protocols 2016](https://pubmed.ncbi.nlm.nih.gov/27560178/). For detailed implementation guidance, see the [Cell Painting wiki](https://broad.io/cellpaintingwiki).

## Available Components

From 12 sources (data-generating centers):

- Raw microscopy images  
- CellProfiler analysis output  
- Single-cell profiles  
- Well-aggregated profiles (all single cells in a given sample well)  
- Metadata files

### Data Processing Levels

1. **Images**  
     
   - 5 channels (DNA, RNA, ER, AGP, Mito) per imaging site within a well  
   - Multiple sites (images) per well

   

2. **CellProfiler Output**  
     
   - Cell segmentation images  
   - Image-level quality metrics

   

3. **Profile Data**  
     
   - Single-cell level profiles  
   - Well-aggregated profiles  
   - Normalized features  
   - Well-aggregated profiles after feature selection applied

   

4. **Index **
   You can find the profile index [here](https://github.com/jump-cellpainting/datasets/blob/main/manifests/profile_index.csv)

   - Parquet tables in which profiles were preprocessed with varying optimized pipelines.
   - The "Interpretable" tables means that they are processed to the point where features retain their original mapping from the original features' names (relating to size, shape, intensity, etc.). In other words, the batch correction step transforms features into a new space so that they no longer reflect their original meanings, so the "Interpretable" profiles are those just before this step. They will not be optimally aligned, but they will still have the original feature meanings.



6. **Processed JUMP reference tables (JUMP_rr tables)**
   [This](https://zenodo.org/records/14046034) dataset provides multiple precomputed analysis tables to make JUMP data exploration accessible:

  - 'X_features.parquet' contains a ranking of the features that distinguish a given perturbation from negative controls.
  - 'X_gallery.parquet' is for visualization of the images with all channels collapsed into one.
  - 'X_cosinesim...parquet' contains the pairwise cosine similarity of all perturbations within a given dataset (i.e., orf, crispr). This allows searching for the closest matches for each perturbation of interest or looking at all relationships in a heatmap.
  - 'X...significance...parquet' is the statistical significance for the phenotypic activity of a given sample (see broad.io/crispr_feature for a formal definition). It shows which perturbations yielded a phenotype distinguishable from negative controls.
  - 'full' tables contain all the data points from the resulting analysis. Their non-full counterpart contains a subset comprised of the most significant entries, meant for in-browser consumption and queries. 
  - Many of the above tables can be interactively viewed using [JUMPrr tools](https://github.com/broadinstitute/monorepo/tree/main/libs/jump_rr#quick-data-access)



## Data Access

### AWS Storage

Hosted in the Cell Painting Gallery ([registry.opendata.aws/cellpainting-gallery/](https://registry.opendata.aws/cellpainting-gallery/)). Access and download is free through AWS Open Data Program.

### Zenodo data

Many of the processed datasets and manifest files can be found associated with the Broad Institute Imaging Platform [community](https://zenodo.org/communities/broad-imaging/records?q=&l=list&p=1&s=10&sort=newest).

### Programmatic Access

- [How-to guides](../howto/0_howto.md) provided  
- APIs and libraries for programmatic access:  
	- [cpgdata](https://github.com/broadinstitute/cpg/tree/main/cpgdata): Tool to generate index of the Cell Painting Gallery files, for faster querying of parquet files using database languages (such as SQL).
  - [jump-portrait](https://github.com/broadinstitute/monorepo/tree/main/libs/jump_portrait): Fetch images using standard gene/compound names into a Python session or filesystem.  
  - [jump-babel](https://github.com/broadinstitute/monorepo/tree/main/libs/jump_babel): Translate perturbation names and access very basic metadata.

## Latest Updates

### Current Status (2024/12)

- All pilot dataset components available  
- Principal dataset: most components available from 12 sources  
- Key metadata files accessible  
- Assembled profile subsets ready for analysis

### Coming Soon

- Extension of metadata and notebooks to pilots ([issue](https://github.com/jump-cellpainting/datasets-private/issues/93))  
- Curated compound annotations from ChEMBL ([issue](https://github.com/jump-cellpainting/datasets-private/issues/78))  
- Deep learning embeddings using pre-trained networks ([issue](https://github.com/jump-cellpainting/datasets-private/issues/50))

### Quality Notes

- Cross-modality matching still being improved (the three modalities are ORF, CRISPR, and chemicals)  
- Some wells/plates/sources excluded for quality control  
- Within-modality matching generally reliable

You can find more details [here](./quirks_details.md).

For the most current updates, subscribe to our [email list](https://jump-cellpainting.broadinstitute.org/more-info).  
