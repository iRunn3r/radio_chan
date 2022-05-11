FROM ubuntu:22.04

# Set up variables
ARG python_ver=python3.10

# Update apt
RUN apt-get update && apt-get -y upgrade

# Install python 3.10
RUN apt install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt -y install $python_ver
RUN apt -y install python3-pip

# Install VLC
run apt -y install vlc

# Install poetry
RUN pip install poetry

# Copy working directory
COPY . .

# Install project Python dependencies
RUN poetry install

# Generate initial playlist
RUN poetry run get-thread
RUN poetry run generate-playlist

RUN useradd -m vlcuser
USER vlcuser

CMD ["cvlc", "--no-video", "--sout", "#transcode{vcodec=none,acodec=vorb,ab=128,channels=2,samplerate=44100}:http{dst=:1410/radio.ogg}", "--no-sout-all", "--sout-keep", "staging/playlist.m3u"]
