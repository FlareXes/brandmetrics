# ---------- BUILDER STAGE ----------
FROM python:3.13-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install build tools for compiling dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first for caching
COPY requirements.txt ./

# Install dependencies into /install
RUN pip install --prefix=/install -r requirements.txt


# ---------- RUNTIME STAGE ----------
FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install only runtime OS dependencies (no compilers)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir gunicorn

# Copy installed Python packages from builder stage
COPY --from=builder /install /usr/local

# Copy app code
COPY ./brandmetrics .

# Expose app port
EXPOSE 8000

# Run with Gunicorn (production WSGI server)
CMD ["gunicorn", "brandmetrics.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
