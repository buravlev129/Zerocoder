FROM ubuntu:22.04

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y apt-utils curl wget bash dos2unix zip unzip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa -y && \
    apt-get update && \
    apt-get install -y python3.12 python3.12-venv && \
    # python3.12-dev
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN python3.12 --version

