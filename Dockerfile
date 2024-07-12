FROM python:3.12.3-slim

WORKDIR /workspace

COPY requirements-dev.txt requirements.txt ./

RUN python -m pip install -r requirements-dev.txt

# RUN apt-get update && apt-get install -y \
#     iputils-ping