FROM python:3.9-slim

WORKDIR /workspace

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
