# Filman

## Introduction
Metagenomic reads can often get contaminated by reads from host(human). These contaminants 
need to be removed before downstream processing and analysis of the datasets. 

Due to the large size of the human genome and metagenomic reads, removing human contaminants
is a computationally challenging problem because the reference genomes are big 
(over 3 billion base pairs long). This task thus requires expansive resources, skills and processing time.

[Latch SDK](https://latch.bio/sdk) has provided an open-source platform to automate workflows thats utilize large CPUs and GPUs,
which eventually expedite processing time and freely available resources.
We have automated `Filman`, a tool to filter human reads from paired-end metagenomics datasets
from a click of a button.

## Steps.
1. Access the tool from this link
2. Upload files through the provided window and launch the workflow.

### Caution
This workflow does not pre-filter poor-quality reads. It is adviced you perform this step before loading data.




