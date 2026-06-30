# syntax=docker/dockerfile:1

FROM python:3.11-slim

WORKDIR /app
ENV FASTAPI_APP=main.py

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "fastapi", "run", "main.py", "--host=0.0.0.0", "--port", "8000"]
