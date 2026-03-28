FROM python:3.13-slim

# Install uv (faster, avoids pip Poetry metadata issues with mcp-memgraph deps)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Default connection to the memgraph service in the same Docker Compose network
ENV MEMGRAPH_URL=bolt://memgraph:7687
ENV MEMGRAPH_USER=""
ENV MEMGRAPH_PASSWORD=""

EXPOSE 8000

CMD ["uv", "run", "--with", "mcp-memgraph", "--python", "3.13", "mcp-memgraph"]
