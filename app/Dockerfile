# Stage 1: build dependencies into a venv (pip, wheels and caches stay here)
FROM python:3.12-slim AS builder
RUN python -m venv /venv
COPY requirements.txt .
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# Stage 2: runtime — only the venv and source, no build tools
FROM python:3.12-slim
RUN useradd --system --uid 10001 app
COPY --from=builder /venv /venv
WORKDIR /srv
COPY --chown=app:app coffee_pos ./coffee_pos
ENV PATH="/venv/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
USER app
EXPOSE 8000
HEALTHCHECK --interval=15s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"
CMD ["uvicorn", "coffee_pos.main:app", "--host", "0.0.0.0", "--port", "8000"]
