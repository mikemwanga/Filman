"""
Filter host (human) reads from sequence data
"""
import subprocess
from pathlib import Path
from latch import small_task, workflow, large_task
from latch.types import LatchFile, LatchDir
from flytekit.types.directory import FlyteDirectory


@large_task
def filter(read1: LatchFile, read2: LatchFile) -> LatchFile:

     #create files
    create = ["touch", "file_1_mapped.bam", "file_1_mapped.sam", "file_1_unmapped.bam", "file_1_unmapped_sorted.bam",
                "file_1_filtered.1.fastq", "file_2_filtered.1.fastq"]

    subprocess.run(create)
   
    mapped_file = Path("file_1_mapped.sam").resolve()
    human_db = Path("humandb").resolve()
    bam_file = Path("file_1_mapped.bam").resolve()
    unmapped_reads = Path("file_1_unmapped.bam").resolve()
    unmapped_reads_sorted = Path("file_1_unmapped_sorted.bam").resolve()
    file1 = Path("file_1_filtered.1.fastq").resolve()
    file2 = Path("file_1_filtered.2.fastq").resolve()

    #create output Directory
    output_DIR = Path("filtered")
    _out_dir = [
        "mkdir",
        "filtered"
    ]
    subprocess.run(_out_dir)

    map = [
        "./bowtie2/bowtie2", 
        "-p", "8", 
        "-x", human_db, 
        "-1", read1, 
        "-2", read2, 
        "-S", mapped_file
        ]
    #subprocess.run(map)


    convert_bam = [
        "samtools", 
        "view",
         "-bS", 
         mapped_file,
         "-o", 
         bam_file
        ]
    subprocess.run(convert_bam)


    extract = [
        "samtools",
        "view",
        "-b", "-f", "12", "-F", "256", 
        bam_file, 
        "-o", unmapped_reads]
    subprocess.run(extract)
    sort = [
        "samtools",
        "sort",
        "-n", unmapped_reads,
        "-o", unmapped_reads_sorted
    ]
    subprocess.run(sort)

    get_fastq = [
        "bedtools",
        "bamtofastq",
        "-i", unmapped_reads_sorted,
        "-fq", file1, 
        "-fq2", file2
    ]
    subprocess.run(get_fastq)

    return (
        LatchFile(str(file1), f"latch://{file1}"), 
        LatchFile(str(file2), f"latch://{file2}"))


@workflow
def filman(read1: LatchFile, read2: LatchFile) -> LatchFile:
    """Filter host (human) reads from seqeunce data

    ### Goal
    This short workflow is meant to enable filtering of human reads (host) from a paired-end read datasets.
    Metagenomic reads can often get contaminated by reads from host(human). These contaminants 
    need to be removed before downstream processing and analysis of the datasets. 

    Due to the large size of the human genome and metagenomic reads, removing human contaminants
    is a computationally challenging problem because the reference genomes are big 
    (over 3 billion base pairs long). This task that requires expansive resources, skills and processing time.

    [Latch SDK](https://latch.bio/sdk) has provided an open-source platform to automate workflows thats utilize large CPUs and GPUs,
    which eventually expedite processing time and freely available resources.
    We have automated Filman, a tool to filter human reads from paired-end metagenomics datasets
    from a click of a button.

    ### Steps.
    1. Access the tool from this link
    2. Upload files through the provided window and launch the workflow.

    ### Caution
    This workflow does not pre-filter poor-quality reads. It is adviced you perform this step before loading data.



    __metadata__:
        display_name: FilMan
        author:
            name: Mike Mwanga
            email: mikemwanga6@gmail.com
            github: https://github.com/mikemwanga/FilMan
            repository: 
            license:
                id: MIT
    Args:

        read1:
          Paired-end read 1 file.

          __metadata__:
            display_name: Read1

        read2:
          Paired-end read 2 file.

          __metadata__:
            display_name: Read2
    """
    return filter(read1=read1, read2=read2)