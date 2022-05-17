# STAGE 1: Create base image

FROM python:3.8-slim-buster as base

WORKDIR /app

COPY . ./

RUN pip install --no-cache-dir --upgrade pip \ 
    && pip install --no-cache-dir -r requirements.txt