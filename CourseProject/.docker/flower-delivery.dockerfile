FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y curl wget bash dos2unix zip unzip mc && \
    apt-get install -y --no-install-recommends nginx && \
    apt-get install -y supervisor && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN mkdir -p storage logs admin

COPY FlowerDelivery ./FlowerDelivery
COPY supervisord.conf /app/supervisord.conf
COPY nginx.conf /etc/nginx/nginx.conf
COPY admin_scripts ./admin
COPY requirements.txt .


RUN python3.12 -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install gunicorn && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt


EXPOSE 8000
EXPOSE 80

CMD ["/bin/bash", "-c", "supervisord -c /app/supervisord.conf"]
