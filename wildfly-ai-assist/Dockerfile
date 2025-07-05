# ---------- build stage ----------------------------------------------------
FROM python:3.11-slim AS builder

WORKDIR /app
COPY pyproject.toml .
RUN pip install poetry
COPY . .
RUN poetry export -f requirements.txt --without-hashes > requirements.txt

# ---------- runtime stage --------------------------------------------------
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000"]
