# syntax=docker/dockerfile:1
FROM ubuntu:latest
WORKDIR .
RUN set -xe \
    && apt-get update \
    && apt-get install python3-pip
COPY requirements.txt requirements.txt
# RUN apt install xorg-dev libx11-dev libgl1-mesa-glx
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python", "main.py"]