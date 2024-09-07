FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY . /app
COPY requirements.txt /requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /requirements.txt

