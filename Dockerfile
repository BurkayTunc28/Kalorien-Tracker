FROM python:3.12-alpine AS builder
WORKDIR /app
RUN pip install uv
COPY uv.lock pyproject.toml ./
RUN uv export --no-dev --format requirements.txt --no-hashes --no-header --no-annotate > requirements.txt

FROM python:3.12-alpine
WORKDIR /app
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -rf /root/.cache
RUN rm -rf /tmp/*
RUN rm -rf /app/requirements.txt
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY ./app ./
EXPOSE 8100
ENTRYPOINT ["fastapi", "run", "main.py"]
CMD ["--port", "8100"]













# EXPOSE 8100
# 