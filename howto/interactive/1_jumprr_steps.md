# JUMP_rr tutorial
## **Step-by-step tutorial: Using JUMP_rr to answer key biological questions**

<div style="text-align: justify;">
The JUMP_rr interactive [tools](https://github.com/broadinstitute/monorepo/tree/main/libs/jump_rr#quick-data-access) allow you to explore the JUMP dataset of genetic and chemical perturbations and their effects on cell morphology features. By applying different filters, you can investigate how specific perturbations influence cells, their structures, and the strength of the changes.

In this tutorial, you will learn how to:

**Step 1: Understand the information displayed in the browser.**  
**Step 2: Explore the data to answer the following questions:**

**2.1**. Is my gene in the JUMP dataset?  
**2.2.** Does my gene have a morphological phenotype when overexpressed or knocked down by CRISPR?  
  **2.2.1.** If yes, what are the specific morphological changes or features?  
  **2.2.2.** What other genes look similar or anticorrelated to my gene?

## **Step 1\. Understand the information displayed in the browser.**

When you open one of the interactive tables, such as the CRISPR knock-outs Feature Ranking [table](http://broad.io/crispr_feature), you will see an informational section explaining the available data columns for that table, and a filtering tool, followed by the data (Figure 1).

<img src="https://zenodo.org/api/records/15252378/files/Figure1.png/content" style="max-width: 100%; height: auto; display: block;">

***Figure 1\.** **Information section of the CRISPR Feature Ranking table.** The red boxes highlight two key components: the first provides definitions for each column; the second one shows the tool to filter based on the content values, such as gene name, subcellular compartment or statistical significance associated with each perturbation.*

Below you will find the full table (Figure 2), which displays aggregated results across replicates for each perturbation. A small triangle on one of the columns shows how the data is currently sorted and you can sort by a data column by clicking its header. Clicking again reverses the sort order. For most tables, sorting by corrected p-value from lowest to highest is a helpful view.

<img src="https://zenodo.org/api/records/15252378/files/Figure2.png/content" style="max-width: 100%; height: auto; display: block;">

***Figure 2\.** **The data section of the CRISPR Feature Ranking table, sorted by row ID.** Each column can be sorted in ascending or descending order by clicking on the header. Sorting is applied to one column at a time and is based on the data type: numerical values are sorted by magnitude, while text is sorted alphabetically. The entries displayed in the Feature Ranking table are the 30 most statistically significant features for each gene (Feature Rank), and for each feature, the 30 genes with the most significant values (Gene Rank). A value of 999999 indicates an unassigned entry. How to use and interpret the Feature Ranking table is described in section 2.2.1.*
</div>

## **Step 2: Explore the data to answer the following questions:**

### **2.1. Was my gene tested in the JUMP collection of perturbations?**

<div style="text-align: justify;">
The JUMP Hub includes a reference tool (Figure 3\) to quickly check whether a specific gene is included in any of the catalogued genetic perturbation datasets, including the JUMP CRISPR and ORF datasets that are available via JUMP_rr tables. You can click on the 'Available Genes' tab in the sidebar from the [JUMP Hub](https://broad.io/jump) page. Heer, you can type the name of the gene of interest to search. Although all gene names in the tool are displayed in capital letters, the search is not case-sensitive. However, the tool does not recognize synonyms or alternative gene names, so queries must match the official gene symbols used in the datasets. The number of occurrences in multiple JUMP or JUMP-adjacent morphological profiling datasets will be displayed: “crispr” and “orf” are the JUMP knock-outs and over expression datasets, “A549”, “HeLa_DMEM” and “HeLa_HPLM” relate to the [PERISCOPE](https://github.com/broadinstitute/2022_PERISCOPE) dataset, and [Lacoste](https://github.com/carpenter-singh-lab/2024_LacosteHaghighi_Cell_Mislocalization) to a dataset focusing on pathogenic coding variants. This tool is especially useful when you want to collate data from multiple morphology-based datasets.

Note that 12,609 genes were tested in the JUMP ORF dataset (larger genes do not express well, so this is roughly the maximum that could be tested) and 7,975 genes were tested in JUMP CRISPR dataset (due to resource limitations). Overall, 15,243 unique human genes were tested in one or the other datasets (or both), giving a \~75% chance your gene was tested in JUMP.

<img src="https://zenodo.org/api/records/16878487/files/Figure3.png/content" style="max-width: 100%; height: auto; display: block;">

***Figure 3\.** **Querying the glucose transporter gene SLC2A in JUMP datasets using the “Available genes” tool.** Overview of the gene reference tool (red box on the left), to quickly check  whether your gene of interest is available in the dataset. You can search using the full name or partial name of a gene in the search window (red box on the right). For each gene, the tool displays how many times it appears in the JUMP dataset under different perturbation types, such as CRISPR (for gene knock-out) and ORF (for overexpression), as well as across information related to the PERISCOPE (A549, HeLa\_DMEM and HeLa\_HPLM) and Lacoste datasets.*
</div>

### **2.2. How does my gene look? And how its corresponding negative controls look?**
<div style="text-align: justify;">
We will identify then plates in which our perturbation of interest is present, and then select the plates in which it is present. Finally we add the negative controls, which are different between genetic perturbations (ORF or CRISPR datasets) and the chemical ones (Compounds dataset). This applies to the CRISPR/ORF/Compound galleries (e.g., [broad.io/crispr_gallery](https://broad.io/crispr_gallery)).

1. Select the column "Perturbation".
2. Select the "in" filter and your perturbation of interest (e.g., MYT1).
3. Click on "Apply" to apply the filter.

<img src="https://zenodo.org/api/records/16878778/files/gallery_negcon_123.png/content" style="max-width: 100%; height: auto; display: block;">
Figure 1: Steps 1-3 of the method to visualize negative controls in the galleries.

4. Select the column "Plate".
5. Select the "in" filter.
6. Copy and paste the different plates shown in the "Plate" column, comma separated.
7. Add the control for the fielderturbation names, sepparated by commas, based on the table:
   - ORF/CRISPR: no-guide,non-targeting
   - Compound: IAZDPXIOMUYVGZ-UHFFFAOYSA-N
8. Click on apply
9. After the new filters are applied, click on "Perturbation" for alphabetical sorting, press it once or twice until your perturbation of interest is at the top. Now you can scroll down to find the controls.

<img src="https://zenodo.org/api/records/16878778/files/gallery_negcon_456789.png/content" style="max-width: 100%; height: auto; display: block;">
**Figure 2.** Steps 4-9 of the method to visualize negative controls in the galleries.

</div>

### **2.3. Does my gene of interest produce a morphology phenotype when overexpressed or knocked down by CRISPR?**

<div style="text-align: justify;">
To answer this question, you will start by exploring the **CRISPR knock-out dataset** to identify genes whose loss affects the phenotype of interest. Then, you will use the ORF overexpression dataset to contrast results with gene overexpression. Of the 15,243 genes tested in JUMP, 68% (10,352) yielded a detectable phenotype (statistically significant “phenotypic activity”), that is, an image-based profile with a signal distinct from negative controls by ORF, CRISPR, or both.

To begin exploring these morphological phenotypes, navigate to the **“How to Guide → Interactive Tools”**. Then, click on the **“JUMP_rr tools”** option, this will take you to the repository where the interactive tables are hosted. Once in the repository, scroll down to the **“Quick Data Access”** section. There, you’ll find links to the CRISPR, ORF, and Compound datasets. Click on the table of interest in the **“Feature Ranking”** column to see the morphological features associated with each perturbation. You can also directly access the feature ranking tables using the following short links:

* [CRISPR knock-out feature table](http://broad.io/crispr_feature)
* [ORF overexpression feature table](http://broad.io/orf_feature)
* [Compound feature table](http://broad.io/feature)

***Search for your gene in the CRISPR dataset.***

Click on the “Feature Ranking” link for the CRISPR knock-down dataset to open a table displaying the morphological features associated with each gene perturbation. From there, you can use the filtering tools to search for your gene of interest and sort the data by criteria such as statistical significance or subcellular compartment. This view helps you determine whether a gene perturbation induces detectable phenotypic changes, and reveals the specific morphological features altered in the cells.

Let us explore data related to the SLC2A2 gene. This gene encodes a glucose transporter primarily expressed in organs such as liver, pancreas and intestine. It plays a key role in glucose sensing and homeostasis. Given its involvement in metabolic processes, changes in SLC2A2 activity or expression could have significant phenotypic consequences that may be captured in image-based profiling data. 

To look for this you can use the Filter Tool, which helps narrow down the dataset based on specific search criteria. When you open the filter menu, a list of all available column names will appear (Figure 4A). In this case, you would select the "Perturbation" column, use the default operator “=”, and enter “SLC2A2” in the search field to display only the rows associated with that gene (Figure 4B).

If you're unsure of the exact name used in the dataset, we recommend make your search case-insensitive by changing the default filter operator from “=” to “like”, and entering a pattern that partially matches a text string, such as “SLC2A%”, since “%” act as a wildcard representing any characters (Figure 4C).

You can also search for alternative names commonly used in the literature. To do this, select the "Synonyms" column, change the filter operator to “contains” or “like”, and enter an alternative name such as GLUT2, or another known synonym of your compound of interest (Figure 4D).

<img src="https://zenodo.org/api/records/15252378/files/Figure4.png/content" style="max-width: 100%; height: auto; display: block;">

***Figure 4\.** **Common filtering methods that can be used in the Feature Ranking table**. Panel A shows the full list of columns available for custom filtering, including metadata such as Corrected p-value, Compartment, and others that support more advanced queries beyond gene-level filtering. B and C illustrate how the number of entries returned depends on the filter type: a broader search using partial names (e.g., “SLC2A%”) yields more entries than an exact match (e.g., “SLC2A2”), which can help identify related genes within the same family. D highlights the utility of the Synonyms column, which maps alternative gene names used in the literature, especially useful for genes with multiple aliases or legacy names not directly listed under the Perturbation column.*
</div>

The table below describes the available logical operators (Table1).

| Operator | Description |
| ----- | ----- |
| \= | Selects results that exactly match the specified value. |
| \!= | Excludes results that exactly match the specified value. |
| contains | Searches for values that include a specific string within the text. |
| ends with | Selects values that end with a specific string. |
| starts with | Selects values that start with a specific string. |
| \> | Selects numeric values greater than the specified value. |
| ≥ | Selects numeric values greater than or equal to the specified value. |
| \< | Selects numeric values less than the specified value. |
| ≤ | Selects numeric values less than or equal to the specified value. |
| like | Searches for patterns that partially match a text string (e.g., “SLC%”). |
| not like | Excludes results that partially match a specific pattern. |
| in | Selects rows where the column value is within a specified list of values. |
| not in | Excludes rows where the column value is within a specified list of values. |
| is blank | Filters rows where the value is an empty string or space — the field exists but has no visible content. |
| is not blank | Filters rows where the field contains visible content (text, numbers, etc.), excluding empty or space-only values. |

<div style="text-align: justify;">

***Table 1\.** **Filtering operators can be used to refine values displayed in the dataset**. Include or exclude rows based on specific conditions, such as matching exact values, checking for patterns in text, or evaluating numerical comparisons.*

You can combine multiple filters. If you want to filter for several values within the same column for example, multiple compartments or gene names, select the appropriate column, choose the **'in'** operator, and enter a list of values separated by commas (e.g., 'Cytoplasm, Nuclei') (Figure 5). Once the filters are applied, you can copy the filtered table by clicking the JSON hyperlink (Figure 5, red box). To export the content, press Ctrl+A to select all, then Ctrl+C to copy it, and finally paste it into a text editor. Note that export as a "CSV" option is not yet available.

<img src="https://zenodo.org/api/records/15252378/files/Figure5.png/content" style="max-width: 100%; height: auto; display: block;">

***Figure 5\.** **Combined filters and export options that can be used to explore and integrate gene-related data.** Example of combined filters applied to display gene-related data for SLC2A2 limited to the “Cells” and “Nuclei” compartments. The red box highlights available export options, such as JSON, which can streamline the integration of filtered results into external analysis pipelines or visualization tools.*

After applying the filter for the **SLC2A2** perturbation, you can evaluate whether the perturbation is significantly different to the negative control condition by examining the **Corrected p-value** column. The Corrected p-value represents the statistical significance of how distinctive the overall morphological profile of a perturbation is when compared to the negative control (after false discovery rate correction). In this case, the corrected p-value is **0.00018**  (all rows display the same value in that column, because this value is computed per perturbation, not per feature). This value (p-value\<0.05) indicates a significant difference from the control condition, suggesting that knocking out **SLC2A2** induces a strong and consistent morphological effect (Figure 6).

<img src="https://zenodo.org/api/records/15252378/files/Figure6.png/content" style="max-width: 100%; height: auto; display: block;">

***Figure 6\.**  **Corrected p-value that can be used to prioritize perturbations with significant morphological effects** The user interface displays the “Corrected p-value” for SLC2A2, which is calculated at the perturbation level. As a result, all rows associated with the SLC2A2 perturbation share the same value (0.00018). When exploring multiple perturbations, sorting by Corrected p-value (or filtering based on it) can help prioritize those with the most statistically significant morphological effects, making it a useful strategy for identifying relevant information. The rows are sorted in ascending/descending order by clicking the name column header.*
</div>

### **2.3.1. What are the specific morphology changes/features?**
<div style="text-align: justify;">
In this section you will be able to identify which features are the most statistically significant within a perturbation. In this filtered view of the SLC2A2 perturbation, all values in the **Feature significance** column are **0.0,** which corresponds to values rounded to five decimal places and  indicates that each listed morphological feature is statistically significant when compared to the control condition (Figure 7). If you'd like more information about the features extracted by CellProfiler, such as how they’re named, you can check out the “*How Measurements are Named*” section in [CellProfiler Handbook](https://cellprofiler-manual.s3.amazonaws.com/CellProfiler-4.0.4/help/output_measurements.html).

<img src="https://zenodo.org/api/records/15252378/files/Figure7.png/content" style="max-width: 100%; height: auto; display: block;">

***Figure 7\.** **Top features that can be sorted and prioritized based on Feature Significance for the SLC2A2 perturbation in the JUMP CRISPR dataset.** Top four features from the filtered CRISPR dataset are sorted in ascending order based on the Feature Significance column (highlighted with a red box). All p-values in this column are displayed as 0.0, which reflects values approximated to five decimal places (i.e., \< 0.00001). Because many features share these low values, we recommend using **Feature Rank** to prioritize features, as it provides their relative importance for each perturbation.*

***Search for your gene in ORF dataset.***

To explore whether overexpressing SLC2A2 produces a morphological phenotype, you will repeat the same filtering process in the ORF overexpression dataset’s Feature Ranking table, link [here](http://broad.io/orf_feature). Using the Filter Tool, you will select the Synonyms column, keep the operator as "=", and enter “SLC2A2” in the search field. 

After filtering, you can examinate the **Corrected p-value** column. In this case, the value is **0.09482**, which is above the 0.05 threshold, indicating that overexpressing *SLC2A2* does not produce a statistically significant morphological change. This contrasts with the CRISPR knock-out dataset, where the loss of *SLC2A2* resulted in a strong and significant phenotypic effect.

However, in the case of SLC2A2, it is still possible to identify individual morphological features that are statistically significant, even if the overall perturbation does not show significant changes compared to the control. In this filtered view, a few features have **Feature Significance** values below 0.05, indicating meaningful differences relative to the control condition (Figure 8).These p-values are corrected for multiple hypothesis testing.

<img src="https://zenodo.org/api/records/15252378/files/Figure8.png/content" style="max-width: 100%; height: auto; display: block;">

***Figure 8\.** **Top features that can be sorted and prioritized based on Feature Significance for the SLC2A2 perturbation in the JUMP ORF dataset.** The top features from the filtered dataset are sorted in ascending order based on the JUMP ORF Feature Ranking table, based on feature significance (per-feature p-values), ranked in increasing order, indicating statistically significant differences compared to the control condition. The Channel and Suffix columns are empty because these features solely come from an object mask and not a fluorescence image. The rows are sorted in ascending/descending order by clicking the name column header.*
</div>

### **2.3.2. What other genes look similar or anti-similar to my genes?**

<div style="text-align: justify;">
Before exploring which perturbations produce the most similar or anti-similar image-based profile (i.e., features that are high in one are lower in the other one), it's important to understand the broader context and potential of image-based profiling. 

Morphological profiles can cluster genes into biologically meaningful groups, uncovering known pathways and revealing functional connections, such as a regulatory interaction between pathways (Rohban et al. 2017). This clustering is based on the similarity of high-dimensional morphological features extracted from images after gene overexpression or CRISPR knock-out. Comparing these profiles systematically can also identify *anti-correlated* perturbations, such as cases where one perturbation produces the opposite phenotype of another (Rohban et al., 2022).  This is particularly relevant for therapeutic discovery, as finding antagonistic morphological profiles may highlight candidate compounds or genes that *suppress* an undesired phenotype.

The "matches” table thus quantifies correlation (or anticorrelation) of profiles and is a powerful resource to uncover potential functional relationships between genes, explore unknown gene roles, or identify suppressors or enhancers within a biological pathway (Chandrasekaran et al., 2024; Ramezani et al., 2025). These insights can help prioritize follow-up experiments and hypothesis generation, especially when analyzing genes or perturbations with poorly characterized functions.

To analyze the SLC2A2 perturbation in the CRISPR matches [table](http://broad.io/crispr), begin by opening the **Filter** menu. From the list of available columns, select **"Perturbation"**, choose the **“like”** operator, and type **"SLC2A2"** in the search field. Then, sort the **"Perturbation-Match Similarity"** column in **descending order** by clicking on the name in that column to view the perturbations with the strongest phenotypic similarity at the top (Figure 9). The similarity scores range theoretically from \-1 (strong anti-similarity) to 1 (strong similarity), although values above 0.8 and below \-0.8 are rarely seen, and values above 0.3 and below \-0.3 tend to indicate a reliable “match”. Typically, scores above 0.3 and below \-0.3 indicate a reliable “match” or “anti-match.” As observed in Section 2.2 *Search for your gene in the CRISPR dataset*, SLC2A2 knock-out displays a strong phenotypic effect, and when compared to other perturbations, a wide range of similarity scores is observed, from a maximum of 0.621, strong phenotypic similarity \- a “match”, to a minimum of \-0.513, strong phenotypic anti-similarity \- an “anti-match” (Figure 9, red box). **The “Perturbation example images” and “Match example image”** shown in the table are randomly sampled from replicates across the experiment (not necessarily from the same plate or batch as the match), providing an unbiased visual representation of each condition. The “Match resources column links to external databases where additional information about the matching/anti-matching gene can be explored (Figure 9, blue box). These images are also useful to check for technical artifacts (e.g., out-of-focus fields, staining issues) or abnormal cell counts (too few or too many cells), which may affect the interpretation of the morphological phenotype.

Now, let’s analyze the SLC2A2 overexpression in the ORF matches table to explore the matches there. Start by opening the **Filter** menu. From the list of available columns, select **"Perturbation"**, choose the **“like”** operator, and enter **"SLC2A2"** in the search field. Next, sort the **"Perturbation-Match Similarity"** column in descending order by clicking on its header as you did for the CRISPR table. In this case, the range of similarity scores is narrower than in the CRISPR dataset, spanning approximately from **0.27** to **\-0.223**. This limited dynamic range may reflect the fact that *SLC2A2* overexpression induces a weaker morphological phenotype compared to its knock-out as you explored in the Section 2.2.1. *Search for your gene in the ORF dataset.*

Taken together, these comparisons provide a starting point for hypothesis generation and pathway exploration, particularly when integrating multiple types of perturbations.

<img src="https://zenodo.org/api/records/15252378/files/Figure9.png/content" style="max-width: 100%; height: auto; display: block;">

***Figure 9\.** **Comparison between the selected perturbation, SLC2A2, in the CRISPR Match table.** After filtering for SCL2A2, the top 4 strongest matches are shown. The Perturbation-Match Similarity column (red box) indicates how similar or anti-similar each perturbation is to SLC2A2 (click on column name to sort it). The Match Resources column (blue box) provides external links to databases with additional information about the genes being compared. The merged images of all Cell Painting channels for SLC2A2 and its matched perturbation can be inspected in the "Perturbation example image" and "Match example image" columns, allowing visual assessment of their morphological signatures to  visual comparison of morphological signatures and potential technical artifacts.* 

**References:**

Mohammad Hossein Rohban, Shantanu Singh, Xiaoyun Wu, Julia B Berthet, Mark-Anthony Bray, Yashaswi Shrestha, Xaralabos Varelas, Jesse S Boehm, Anne E Carpenter (2017) Systematic morphological profiling of human gene and allele function via Cell Painting eLife 6:e24060

Mohammad H. Rohban, Ashley M. Fuller, Ceryl Tan, Jonathan T. Goldstein, Deepsing Syangtan, Amos Gutnick, Ann DeVine, Madhura P. Nijsure, Megan Rigby, Joshua R. Sacher, Steven M. Corsello, Grace B. Peppler, Marta Bogaczynska, Andrew Boghossian, Gabrielle E. Ciotti, Allison T. Hands, Aroonroj Mekareeya, Minh Doan, Jennifer P. Gale, Rik Derynck, Thomas Turbyville, Joel D. Boerckel, Shantanu Singh, Laura L. Kiessling, Thomas L. Schwarz, Xaralabos Varelas, Florence F. Wagner, Ran Kafri, T.S. Karin Eisinger-Mathason, Anne E. Carpenter (2022) Virtual screening for small-molecule pathway regulators by image-profile matching. *Cell Systems*, 13(9): 724–736.e9.

Srinivas Niranj Chandrasekaran, Eric Alix, John Arevalo, Adriana Borowa, Patrick J. Byrne, William G. Charles, Zitong S. Chen, Beth A. Cimini, Boxiong Deng, John G. Doench, Jessica D. Ewald, Briana Fritchman, Colin J. Fuller, Jedidiah Gaetz, Amy Goodale, Marzieh Haghighi, Yu Han, Zahra Hanifehlou, Holger Hennig, Desiree Hernandez, Christina B. Jacob, Tim James, Tomasz Jetka, Alexandr A. Kalinin, Ben Komalo, Maria Kost-Alimova, Tomasz Krawiec, Brittany A. Marion, Glynn Martin, Nicola Jane McCarthy, Lisa Miller, Arne Monsees, Nikita Moshkov, Alán F. Muñoz, Arnaud Ogier, Magdalena Otrocka, Krzysztof Rataj, David E. Root, Francesco Rubbo, Simon Scrace, Douglas W. Selinger, Rebecca A. Senft, Peter Sommer, Amandine Thibaudeau, Sarah Trisorus, Rahul Valiya Veettil, William J. Van Trump, Sui Wang, Michał Warchoł, Erin Weisbart, Amélie Weiss, Michael Wiest, Agata Zaremba, Andrei Zinovyev, Shantanu Singh, Anne E. Carpenter (2024) Morphological map of under- and over-expression of genes in human cells. bioRxiv. https://doi.org/10.1101/2024.12.02.624527

Ramezani, M., Weisbart, E., Bauman, J. et al. A genome-wide atlas of human cell morphology. Nat Methods 22, 621–633 (2025). https://doi.org/10.1038/s41592-024-02537-7

</div>
