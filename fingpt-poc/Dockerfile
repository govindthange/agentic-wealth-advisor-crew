FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# This version allows the shell to expand the variables from the .env file
CMD uvicorn server:app --host $SERVER_HOST --port $SERVER_PORT
