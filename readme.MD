# README

**Mapping between Human Phenotype Ontology terms (HPO) and Phecodes (organizations of ICD codes) to link rare and common disease vocabularies**

Created: April 20, 2022

Created By: Evonne McArthur

Last Edited: Dec 12, 2022


# About

- Code and data for Evonne McArthur, Lisa Bastarache, John A Capra, Linking rare and common disease vocabularies by mapping between the human phenotype ontology and phecodes, JAMIA Open, Volume 6, Issue 1, April 2023, ooad007, https://doi.org/10.1093/jamiaopen/ooad007
- Most of the analysis was done in the was done in the `bin/format_data_and_extract_phecodeHPO_mapping.ipynb` and figure-generation was done in the `bin/explore_phecodeHPO_mapping_make_figures.ipynb` with python 3.6.3 (see dependencies in `bin/environment.yml`). It is not recommended to run this notebook from start-to-finish, but to run individual sections for the analysis you want to replicate. All resources are all linked and cited in the methods section of the paper (section “Data availability”)


# Looking for the final phecode-hpo mappings?

- Final mappings (including unfiltered links) are in `./data/finalHPO-phecodeLinks/`. See below in the manifest for more details about each file.
- The mappings have been filtered for diverse needs. Please use this flowchart (Fig 2 in the paper) as reference:

    <img src="https://raw.githubusercontent.com/emcarthur/phecode-HPO-map/main/flowchart_full.png" width="800" >

- Each of these files are in `./data/finalHPO-phecodeLinks/mapsFromFlowchart/`
- These have also been formatted for use in the PheRS R package here `./data/finalHPO-phecodeLinks/mapsFromFlowchart/pheRSpackage/`
- If you are looking for the "strong specific" or "strong broad" filtered maps, they are here `data/finalHPO-phecodeLinks/mapsFilteredByEvidenceType/` (including those formatted for PheRS)

# Manifest

## `bin/`: scripts
- `format_data_and_extract_phecodeHPO_mapping.ipynb` - Ipython/Jupyter notebook in python for data preprocessing/formatting, analysis, and creating the mapping. It is organized by sub-section and figure to align with the presentation of results from the paper. Other python scripts are also launched from this notebook so if you want example usage for the other python scripts (below), check this out. Sections include:
    
    <img src="https://raw.githubusercontent.com/emcarthur/phecode-HPO-map/main/github_toc_data.png" width="350" >
    
- `explore_phecodeHPO_mapping_make_figures.ipynb`:  Ipython/Jupyter notebook in python for data visualization/plotting. It is organized by sub-section and figure/tables to align with the presentation of results from the paper. Sections include:

    <img src="https://raw.githubusercontent.com/emcarthur/phecode-HPO-map/main/github_toc_figs.png" width="400" >

- `environment.yml`- List and version of packages/dependencies used in Anaconda environment for all python scripts in this project
- `parallelStringMapping.sh` and `mapping.py`: Python script and slurm shell script to parallelize string/substring matching and WikiMedMap procedures. mapping.py usage: mapping.py [-h] -f FROM -t TO -m MAP -o OUTPUT [--i I] (Options for -m include string substring or wikimed, Options for the from/to term include phecodeX phecode 1.2 ICD9 ICD10 hpo, the -I takes an index range for a subset of the file that is used to parallelize over in the slurm array). The wikimedmap code is modified from https://github.com/Linasulieman/WikiMedMap/ (major change includes auto_suggest=False instead of the default True)

## `/data/raw`: raw data, data for formatting, and unformatted manual mappings
- `hp.owl`: Download hpo ontology with `wget https://raw.githubusercontent.com/obophenotype/human-phenotype-ontology/master/hp.owl`
- `phecode_definitions1.2.csv.zip`: Downloaded Phecode Map 1.2 from https://phewascatalog.org/phecodes with `wget https://phewascatalog.org/files/phecode_definitions1.2.csv.zip`
- `4-8-22PheWAS_translate_PhecodeX_strings.csv`, `4-8-22PheWAS_translate_PhecodeX_ICD_to_phecode.csv`, : Latest Phecode X information from Lisa Bastarache (older/other versions found here https://phewascatalog.org/phecode_x)
- `phecode_icd9_map_unrolled.csv.zip`: `wget https://phewascatalog.org/files/phecode_icd9_map_unrolled.csv.zip`
- `phecode_icd9_rolled.csv`: Export all ICD9 (not CM) and phecode links from the table here https://phewascatalog.org/phecodes (on 4/20/2022)
- `phecode_icd10.csv`: Export all ICD10 (not CM) and phecode links from the table here https://phewascatalog.org/phecodes_icd10 (on 4/20/2022) 
- `ICD-CM to phecode, unrolled.txt`: from phewas website https://phewascatalog.org/phecodes_icd10cm (needed for links between phecodes and ICD codes)
- `icd10cm_order_2022.txt` - https://www.cms.gov/medicare/icd-10/2022-icd-10-cm (2022 Code Descriptions in Tabular Order - Updated 02/01/2022 (ZIP)) (needed for ranges of phewas from UMLS)
- `4-22-22mapsR_package_HPO_anno_view_for_Evonne.csv`: manually created map by LB (phecode 1.2)
- `4-13-22mapsR_package_HPO_anno_phecodeX_view_for_Evonne.csv`: manually created map by LB (phecode X)
- `MRCONSO.RRF.gz`: Concept names and sources from UMLS Metathesaurus 2022AA release from: https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html (You must create your own account and download)
- `MRREL.RRF.gz`: Relationships from UMLS Metathesaurus 2022AA release from: https://www.nlm.nih.gov/research/umls/licensedcontent/umlsknowledgesources.html (You must create your own account and download)
- `PheMap_UMLS_Concepts_1.1.csv`: From https://www.vumc.org/cpm/phemap%20PheMap%20v1.1(07/07/20) (The raw PheMap knowledgebase containing weighted concepts with CUIs from UMLS. CUI: from UMLS, TFIDF: Weighted PheMap score for concept)
- `SORTA/input`: Text files generated in `bin/format_data_and_extract_phecodeHPO_mapping.ipynb` for intput into SORTA chunked into files with 5000 terms (ICD9/10 or Phecode)
- `SORTA/output`: Raw SORTA output from Molgenis Cloud (https://sorta.molgeniscloud.org/menu/main/sorta)

## `data/`: processed codes and labels used for maps
All of these files were generated in `bin/format_data_and_extract_phecodeHPO_mapping.ipynb`
- `hpo.tsv`: Human Phenotype ontology codes + synonyms
- `phecode1.2.tsv`: Phecode 1.2 codes
- `phecodeX.tsv`: Phecode X codes
- `ICD9.tsv`: ICD9 codes and their links to phecodes
- `ICD10.tsv`: ICD10 codes and their links to phecodes
- `ICD9_labels.tsv`: labels/names of ICD10 codes from MRCONSO.RRF (UMLS database) and phecode_icd9_rolled.csv
- `ICD10_labels.tsv`: labels/names of ICD10 codes from MRCONSO.RRF (UMLS database) 

## `data/evidenceTables`
Formatted tables of evidence linking together HPO and phecode/ICD organized by evidence type. All files created were created `bin/format_data_and_extract_phecodeHPO_mapping.ipynb` by reading in raw files/tables described above. If you want to see the particular ICD code that linked a phecode with an HPO term via a particular data type, these would be the files to look in.

## `data/finalHPO-phecodeLinks`
All files created were created `bin/format_data_and_extract_phecodeHPO_mapping.ipynb` by reading in evidence tables described above.
- `hpo-phecode[1.2/X]_links.tsv`: Final HPO-Phecode mapping
- `hpo-phecode[1.2/X]_links_withEvidenceRatings.tsv`: Same as above but with 3 extra columns describing if the link has "strong specific", "strong broad" or "any" evidence. These are tables in the manuscript (S1, S3)
- `hpo-phecode[1.2/X]_links_withHPOchildrenExpansion.tsv`: Same as above but includes links between Phecodes and all the children of the identified HPO code. These are tables in the manuscript (S2, S4)
- `mapsFilteredByEvidenceType/`: Maps that are filtered by levels of evidence ("strong specific" or "strong broad")
- `mapsFromFlowchart/`: Maps that are filtered by evidence optimized based on exploring the precision-recall space of all combinations of evidence types
- `mapsFromFlowchart/PRcalcsForEvidence/`: Exploration of the precision-recall space across all combinations of evidence types. The max F0.5 and F1 scores from these were used to select the combinations of evidence in the flowchart (Fig 2)
- `[mapsFilteredByEvidenceType or mapsFromFlowchart]/pheRSpackage`: Maps that are formatted for the PheRS R package

## `data/manualReview`
- `hpo-phecode[1.2/X]-links[_withHPOchildrenExpansion]_forManualReview.tsv`: The shuffled HPO-phecode links for manual review to assess precision. There are 4 different maps: (Phecode 1.2 and X) x (without children and with children)
- `hpo-phecode[1.2/X]-links[_withHPOchildrenExpansion]_manuallyReviewed.csv`: The 4 maps above but with the top 250 links manually reviewed with a column called "narrower". 0 means no match, M means similar semantic match, P means phecode is a subconcept (narrower) than HPO term, H means HPO term is a subconcept (narrower) than the phecode





