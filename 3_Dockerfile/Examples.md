# Приклади Dockerfile

## 1. Hello World — Python script

Simplest possible Dockerfile — just runs a script

### Dockerfile:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
```

### Script:
```python
# app.py
print("Hello from Docker!")
```

### Build and run:
```bash
docker build -t hello .
docker run hello
```

## 2. Static website — Nginx

Serve a simple HTML page

### Dockerfile:
```dockerfile
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
EXPOSE 80
```

### Page:
```html
<!-- index.html -->
<h1>My site is running in Docker!</h1>
```

### Build and run:
```bash
docker build -t mysite .
docker run -d -p 8080:80 mysite
```

## 3. Python app with dependencies

Install packages before running

### Dockerfile:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### Script:
```python
# app.py
import requests
r = requests.get("https://api.github.com")
print("GitHub status:", r.status_code)
```

### Creating venv and requirements.txt:
```bash
# Створення venv
python -m venv venv

# Запуск venv
venv/Scripts/activate

# Встановлення модуля requests
# (повторити для всіх необхідних модулів)
pip install requests

# Створення файлу requirements.txt
pip freeze > requirements.txt

# Деактивація venv
deactivate
```


### Build and run:
```bash
docker build -t pyapp .
docker run pyapp
```

## 4. Nginx with custom config

Configure Nginx behavior manually

### Dockerfile:
```dockerfile
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY ./site /usr/share/nginx/html
EXPOSE 80
```

### Config:
```nginx
# nginx.conf
events {}
http {
    server {
        listen 80;
        root /usr/share/nginx/html;
        index index.html;

        # Return 404 page for missing files
        error_page 404 /404.html;
    }
}
```
```
site/
├── index.html
└── 404.html
```

### Build and run:
```bash
docker build -t nginxapp .
docker run -d -p 8080:80 nginxapp
```

## 5. Multi-stage build — React app

Build with Node.js, serve with Nginx — professional approach

### Dockerfile:
```dockerfile
# ── Stage 1 — Build React app ──────────────────
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json .
RUN npm install
COPY . .
RUN npm run build

# ── Stage 2 — Serve with Nginx ─────────────────
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Build and run:
```bash
# Create React app first
docker run --rm -v $(pwd):/app -w /app node:20 npx create-react-app myapp

cd myapp
docker build -t reactapp .
docker run -d -p 8080:80 reactapp
```

## 6. ASP.NET Core Web API

### Dockerfile:
```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /source

ENV ASPNETCORE_ENVIRONMENT=Development
ENV ASPNETCORE_URLS=http://+:80

EXPOSE 80
EXPOSE 443

COPY *.sln .
COPY <PROJECT NAME>/*.csproj ./<PROJECT NAME>/
RUN dotnet restore <PROJECT NAME>/<PROJECT NAME>.csproj

COPY <PROJECT NAME>/. ./<PROJECT NAME>/
WORKDIR /source/<PROJECT NAME>
RUN dotnet publish -c release -o /app

FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app ./

ENTRYPOINT ["dotnet", "<PROJECT NAME>.dll"]
```