FROM python:3.12-slim

WORKDIR /workspace

COPY requirements.txt requirements-dev.txt ./

RUN python -m pip install -r requirements-dev.txt
