FROM python:3.14-slim
WORKDIR /app
COPY client.py .
CMD ["python", "client.py"]