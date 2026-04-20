FROM python:3.14-slim
WORKDIR /app
COPY server.py .
CMD ["python", "server.py"]