FROM python:3.10-slim

# Install gettext library and psql client to check whether pg db is available
RUN set -ex \
    && BUILD_DEPS=" \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcairo2 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgdk-pixbuf2.0-0 \
    libglib2.0-0 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libpango-1.0-0 \
    libx11-6 \
    libxcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    libxshmfence1 \
    wget \
    xdg-utils \
    xvfb \
    " \
    && apt-get update && apt-get install -y --no-install-recommends $BUILD_DEPS \
    && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install --upgrade pip && pip install poetry

# Copy dependency files
# To generate poetry files:
# cat requirements.txt | xargs -I % sh -c 'poetry add "%"'
COPY pyproject.toml /
COPY poetry.lock /
#COPY requirements.txt /

# Create requirements.txt file
RUN poetry export -f requirements.txt --output /requirements.txt

# Install dependencies
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt

ENV PATH="/py/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy your application code to the container 
# Note: create a .dockerignore file if any large files or directories should be excluded
RUN mkdir -p /app/src/
WORKDIR /app/
COPY manage.py /app/
COPY api_entrypoint.sh /app/
ADD src /app/src/

# gunicorn will listen on this ports
EXPOSE 80
EXPOSE 443

# Add any custom, static environment variables needed by Django or your settings file here:
#ENV DJANGO_SETTINGS_MODULE=myapp.settings
ENV DJANGO_CONFIGURATION=Prod
ENV WSGI_APLICATION="src.core.wsgi:application"

ENTRYPOINT ["/app/api_entrypoint.sh"]
