# 3. Створення Dockerfile та Docker Image

![alt text](https://miro.medium.com/v2/0*CP98BIIBgMG2K3u5.png)

>**Docker Image (образ)** — це незмінний шаблон, який містить додаток, залежності та налаштування, необхідні для запуску контейнера. Він створюється на основі **Dockerfile**, є read-only (не змінюється під час роботи) та використовується для створення контейнерів
>
>**Dockerfile** — це текстовий файл, який містить набір інструкцій для автоматичного створення Docker-образу. Він описує покроковий процес збірки образу за допомогою таких команд: `FROM`, `RUN`, `COPY`, `CMD`.
>
> Детальніше: https://docs.docker.com/get-started/docker-concepts/the-basics/what-is-an-image/


## 📁 Basic Structure

```dockerfile
# Comment
INSTRUCTION argument
```

- Instructions are written in **UPPERCASE** by convention
- Each instruction creates a new **layer**
- Layers are **cached** — unchanged layers are reused on rebuild

Перелік аргументів можна знайти у файлі [FileInstructions.md](/3_Dockerfile/FileInstructions.md)

---



## 📋 Complete Example — Python Flask App

```dockerfile
# Base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies first (layer caching!)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Set environment variables
ENV FLASK_ENV=production
ENV PORT=5000

# Create non-root user (security best practice)
RUN useradd -m appuser
USER appuser

# Copy application code
COPY . .

# Document port
EXPOSE 5000

# Start the app
CMD ["python", "app.py"]
```

Інші приклади можна знайти у файлі [Examples.md](/3_Dockerfile/Examples.md)

---

## 🏗️ Multi-Stage Build Example

Used to keep the **final image small** by separating build and runtime stages.

```dockerfile
# ── Stage 1: Build ─────────────────────────────
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
RUN npm run build

# ── Stage 2: Serve ─────────────────────────────
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

> 💡 Final image only contains Nginx + built files — **no Node.js, no source code!**

---

## ✅ Best Practices

### 1. Order layers from least to most changed
```dockerfile
# ✅ Dependencies change rarely — cache them early
COPY requirements.txt .
RUN pip install -r requirements.txt

# ✅ Your code changes often — copy it last
COPY . .
```

### 2. Use slim or alpine images
```dockerfile
# ❌ Heavy — ~900MB
FROM python:3.12

# ✅ Light — ~50MB
FROM python:3.12-slim

# ✅ Lightest — ~20MB
FROM python:3.12-alpine
```

### 3. Use `.dockerignore`
Create a `.dockerignore` file to exclude unnecessary files:
```
__pycache__
*.pyc
.env
.git
node_modules
*.log
```

### 4. Never run as root
```dockerfile
RUN useradd -m appuser
USER appuser
```

### 5. One process per container
```dockerfile
# ✅ One container = one responsibility
CMD ["python", "app.py"]     # web app container
# Run database in a separate container!
```

---

## 🔧 Useful Build Commands

```bash
# Build an image
docker build -t myapp .

# Build with specific Dockerfile
docker build -f Dockerfile.prod -t myapp .

# Build without cache
docker build --no-cache -t myapp .

# Pass build argument
docker build --build-arg VERSION=3.11 -t myapp .

# Check image size
docker images myapp
```

## Додаткові матеріали:
- Understand Dockerfile https://medium.com/swlh/understand-dockerfile-dd11746ed183