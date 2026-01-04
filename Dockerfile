# ---------- Frontend Build Stage ----------
FROM node:24.12-alpine3.22 AS frontend-build

WORKDIR /frontend

COPY frontend/package*.json ./
RUN npm ci

COPY frontend .
RUN npm run build


# ---------- Backend Runtime Stage ----------
FROM ghcr.io/astral-sh/uv:python3.12-trixie

# Disable development dependencies
ENV UV_NO_DEV=1

COPY main.py .
COPY .python-version .
COPY pyproject.toml .
COPY uv.lock .
COPY chatter ./chatter
COPY resources ./resources

RUN uv sync --locked

# Copy frontend build output into backend
# Adjust if Vite output directory differs
COPY --from=frontend-build /resources/rendered ./resources/rendered

EXPOSE 8000 4343

CMD ["uv", "run", "main.py"]
