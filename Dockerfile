FROM ubuntu:20.04

LABEL maintainer="VishnuPriya <vishnupriyatr27@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update -qq && \
    apt-get install -y \
    build-essential \
    python3.10 python3.10-dev python3-pip \
    zip unzip openjdk-11-jdk \
    git curl \
    libncurses5 libstdc++6 zlib1g-dev libffi-dev \
    libssl-dev cmake lib32z1 lib32stdc++6 && \
    pip3 install --upgrade pip && \
    pip3 install buildozer cython && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m builduser
USER builduser
WORKDIR /home/builduser/app

COPY . .

RUN buildozer android debug

VOLUME /home/builduser/app/bin
