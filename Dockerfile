# syntax=docker/dockerfile:1

FROM python:3.12-slim AS build
WORKDIR /build

# Install build tools and node for frontend
RUN apt-get update \ 
    && apt-get install -y --no-install-recommends \
        build-essential libdbus-1-dev libglib2.0-dev nodejs npm git \ 
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-dev.txt ./
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --prefix=/install --no-cache-dir -e .
RUN cd webui && npm ci && npm run build

FROM python:3.12-slim
WORKDIR /app

COPY --from=build /install /usr/local
COPY --from=build /build/webui/dist ./webui/dist
COPY --from=build /build/src ./src
COPY --from=build /build/server ./server
COPY --from=build /build/main.py ./

RUN apt-get update \ 
    && apt-get install -y --no-install-recommends libdbus-1-3 libglib2.0-0 \ 
    && rm -rf /var/lib/apt/lists/*

HEALTHCHECK CMD python -m piwardrive.scripts.health_export --check || exit 1

CMD ["piwardrive-webui"]
