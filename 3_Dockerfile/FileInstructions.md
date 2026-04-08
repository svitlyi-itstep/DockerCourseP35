# Інструкції Dockerfile

## 📊 Швидкі посилання

| Instruction | When it runs | Purpose |
|---|---|---|
| `FROM` | Build | Set base image |
| `WORKDIR` | Build | Set working folder |
| `COPY` | Build | Copy files |
| `RUN` | Build | Execute commands |
| `ENV` | Build + Runtime | Set variables |
| `ARG` | Build only | Build-time variables |
| `EXPOSE` | Documentation | Document port |
| `USER` | Build + Runtime | Set user |
| `VOLUME` | Runtime | Declare persistent storage |
| `CMD` | Runtime | Default start command |
| `ENTRYPOINT` | Runtime | Fixed start command |

---

## 🔄 Порядок запуску інструкцій

```
FROM        → pull base image
RUN         → executed during BUILD
COPY        → executed during BUILD
WORKDIR     → executed during BUILD
ENV         → set during BUILD, available at RUNTIME
EXPOSE      → documentation only
USER        → set during BUILD, applies at RUNTIME
CMD         → executed at RUNTIME (container start)
```

---

## Детальний опис

### `FROM` — Base image
**Always the first instruction.** Defines which image to start from.

```dockerfile
FROM python:3.12-slim
FROM node:20-alpine
FROM nginx
FROM ubuntu:22.04
```

> 💡 Use `-slim` or `-alpine` variants for smaller images.

---

### `WORKDIR` — Set working directory
Sets the working folder inside the container. All following instructions run from this folder.

```dockerfile
WORKDIR /app
```

> 💡 Always use `WORKDIR` instead of `RUN cd /app` — it's cleaner and more reliable.

---

### `COPY` — Copy files into image
Copies files from your machine into the container.

```dockerfile
COPY source destination

COPY app.py .                  # copy single file
COPY requirements.txt .        # copy single file
COPY . .                       # copy everything
COPY ./src /app/src            # copy folder
```

> ⚠️ Always copy `requirements.txt` **before** your code — this allows Docker to cache dependencies correctly.

---

### `RUN` — Execute command while building
Runs a command **during the build process.** Used for installing dependencies, creating folders, etc.

```dockerfile
RUN pip install -r requirements.txt
RUN apt update && apt install -y curl
RUN npm install
RUN mkdir -p /app/logs
```

> 💡 Chain commands with `&&` to reduce the number of layers.

```dockerfile
# ❌ Creates 3 layers
RUN apt update
RUN apt install -y curl
RUN apt clean

# ✅ Creates 1 layer
RUN apt update && apt install -y curl && apt clean
```

---

### `CMD` — Default command when container starts
Defines the command that runs **when the container starts.** Can be overridden at runtime.

```dockerfile
CMD ["python", "app.py"]
CMD ["nginx", "-g", "daemon off;"]
CMD ["node", "server.js"]
```

> 💡 Always use **exec form** `["command", "arg"]` instead of shell form `command arg`.

---

### `ENTRYPOINT` — Fixed command when container starts
Similar to `CMD`, but **cannot be overridden** at runtime. Used when the container should always run a specific program.

```dockerfile
ENTRYPOINT ["python"]
CMD ["app.py"]             # default argument, can be overridden
```

```bash
docker run myapp           # runs: python app.py
docker run myapp other.py  # runs: python other.py
```

---

### `EXPOSE` — Document a port
Documents which port the app uses inside the container. **Does not actually publish the port** — that's done with `-p` in `docker run`.

```dockerfile
EXPOSE 5000
EXPOSE 80
EXPOSE 3000
```

> 💡 Think of `EXPOSE` as documentation — it tells other developers which port to map.

---

### `ENV` — Set environment variables
Sets environment variables inside the container. Available both during build and at runtime.

```dockerfile
ENV PORT=5000
ENV FLASK_ENV=production
ENV NODE_ENV=production
```

```bash
# Override at runtime
docker run -e FLASK_ENV=development myapp
```

---

### `ARG` — Build-time variable
Similar to `ENV`, but only available **during the build process**, not at runtime.

```dockerfile
ARG VERSION=3.12
FROM python:${VERSION}-slim
```

```bash
# Pass at build time
docker build --build-arg VERSION=3.11 -t myapp .
```

---

### `VOLUME` — Declare a volume
Marks a directory as a volume — data here **persists outside the container.**

```dockerfile
VOLUME /app/uploads
VOLUME /var/lib/mysql
```

---

### `USER` — Set the user
Sets which user runs the following instructions and the container itself. Important for **security.**

```dockerfile
RUN useradd -m appuser
USER appuser
```

> ⚠️ Never run containers as `root` in production!

---

### `COPY --from` — Copy from another stage
Used in **multi-stage builds** to copy files from a previous build stage.

```dockerfile
COPY --from=builder /app/build /usr/share/nginx/html
```

---
