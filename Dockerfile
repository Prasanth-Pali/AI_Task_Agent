FROM node:20-bullseye AS frontend-build

WORKDIR /app
COPY Frontend/package*.json ./Frontend/
WORKDIR /app/Frontend
RUN npm install
COPY Frontend/ .
RUN npm run build -- --configuration production

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        libpq-dev \
        unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

COPY Backend/requirements.txt ./Backend/requirements.txt
RUN python -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install -r /app/Backend/requirements.txt

COPY Backend ./Backend
COPY --from=frontend-build /app/Frontend/dist ./Frontend/dist

EXPOSE 8000 4200

CMD bash -lc 'FRONTEND_DIR="/app/Frontend/dist/frontend"; if [ ! -d "$FRONTEND_DIR" ]; then FRONTEND_DIR="/app/Frontend/dist"; fi; (cd "$FRONTEND_DIR" && python -m http.server 4200) & /opt/venv/bin/python -m uvicorn Backend.main:app --host 0.0.0.0 --port 8000'
