FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y curl wget bash dos2unix zip unzip mc && \
    apt-get install -y iputils-ping dnsutils && \
    apt-get install -y --no-install-recommends nginx && \
    apt-get install -y supervisor && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

RUN python3.12 -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install gunicorn && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt

RUN mkdir -p storage logs admin
RUN chmod -R 755 /app
RUN chown -R www-data:www-data /app/storage

COPY FlowerDelivery ./FlowerDelivery
COPY supervisord.conf /etc/supervisor/conf.d/flowerdelivery.conf
COPY admin_scripts ./admin

RUN mv /etc/nginx/nginx.conf /etc/nginx/nginx_orig.conf
COPY nginx.conf /etc/nginx/nginx.conf


CMD ["/bin/bash", "-c", "supervisord -c /etc/supervisor/supervisord.conf"]
