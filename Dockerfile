FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:6839-main

RUN apt-get install -y curl unzip

RUN curl https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh --output miniconda.sh
ENV CONDA_DIR /opt/conda
RUN bash miniconda.sh -b -p /opt/conda
ENV PATH=$CONDA_DIR/bin:$PATH
RUN conda install -c bioconda samtools
RUN conda install -c bioconda bedtools
RUN curl -L http://ftp.ensembl.org/pub/release-107/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.toplevel.fa.gz -o Homo_sapiens.GRCh38.dna.toplevel.fa.gz
RUN curl -L https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.4.4/bowtie2-2.4.4-linux-x86_64.zip/download -o bowtie2-2.4.4.zip &&\
    unzip bowtie2-2.4.4.zip &&\
    mv bowtie2-2.4.4-linux-x86_64 bowtie2 &&\
    export PATH=bowtie2/:$PATH

ENV PATH=$bowtie2/:$PATH
RUN ./bowtie2/bowtie2-build Homo_sapiens.GRCh38.dna.toplevel.fa.gz humandb
# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN python3 -m pip install --upgrade latch
WORKDIR /root
