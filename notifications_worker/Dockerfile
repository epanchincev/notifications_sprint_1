FROM python:3.11.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY ./src .

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"] 