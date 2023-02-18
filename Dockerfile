# syntax=docker/dockerfile:1
FROM alpine/doctl
WORKDIR .
ENV PYTHONUNBUFFERED=1

# Update apt packages
# RUN apk update
# RUN apk upgrade -y

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python", "main.py"]