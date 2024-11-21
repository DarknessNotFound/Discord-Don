FROM python:3.12.5-slim-bullseye
LABEL Maintainer="Grant"
WORKDIR /app

RUN pip install --upgrade pip
RUN python3 -m pip install -U python-dotenv
RUN python3 -m pip install -U discord.py

RUN mkdir ./data
RUN mkdir ./cogs
COPY *.py ./
COPY cogs/*.py ./cogs/

CMD  python ./main.py
