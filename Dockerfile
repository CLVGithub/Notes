FROM python:3.14.3-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY entrypoint.sh /app/entrypoint.sh

RUN apt-get update && apt-get install -y vim

ENTRYPOINT ["/app/entrypoint.sh"]
