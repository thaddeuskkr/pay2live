FROM python:slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ADD . /app
WORKDIR /app
RUN uv sync --frozen
CMD ["/app/.venv/bin/waitress-serve", "--listen", "0.0.0.0:5000", "app:app"]