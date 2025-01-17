# Use Python 3.10 slim image as the base
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies required for Poetry and project dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
        make \
        gcc \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="${PATH}:/root/.local/bin"

# Copy poetry configuration files
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create a virtual environment
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --with infer

# Copy the rest of the application code
COPY . .

# Expose port 8000 for the FastAPI application
EXPOSE 8000

CMD make api