# ─────────────────────────────────────────────────────────────────────────────
# Stage 1 — dependency builder
#   Installs all Python packages into /install so the final image only copies
#   compiled wheels (no build tools or pip cache).
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /install

# Copy only the requirements first to leverage Docker layer caching.
COPY requirements.txt .

RUN pip install --upgrade pip \
 && pip install --no-cache-dir --prefix=/install -r requirements.txt


# ─────────────────────────────────────────────────────────────────────────────
# Stage 2 — runtime image
# ─────────────────────────────────────────────────────────────────────────────
FROM python:3.12-slim AS runtime

# Create a non-root user for security.
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

# Copy installed packages from builder stage.
COPY --from=builder /install /usr/local

# Copy application source (excluding files listed in .dockerignore).
COPY --chown=appuser:appgroup . .

# Switch to non-root user.
USER appuser

# Expose the port uvicorn will listen on.
EXPOSE 8000

# Health-check so orchestrators (Docker Compose, k8s) know when the app is ready.
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/docs')"

# Start the FastAPI app.
# --host 0.0.0.0  → accept connections from outside the container.
# --workers 2     → two Uvicorn worker processes (tune as needed).
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
