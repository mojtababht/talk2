FROM python:3.10

WORKDIR /app
COPY chats /app
COPY requirements.txt /requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r /requirements.txt

