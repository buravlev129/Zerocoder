FROM ubuntu:22.04

RUN apt-get update &&\
    apt-get install -y --no-install-recommends python3.12 python3.12-venv python3.12-dev &&\
    apt-get install -y nginx supervisor curl &&\
    apt-get clean &&\
    rm -rf /var/lib/apt/lists/*

# Создание пользователя для запуска приложения и nginx
# RUN useradd -m -s /bin/bash appuser &&\
#     mkdir -p /app &&\
#     chown -R appuser:appuser /app /var/log/nginx /var/cache/nginx /var/run/nginx.pid

# USER appuser

# WORKDIR /app

# COPY --chown=appuser:appuser . /app

# RUN python3.12 -m venv /app/venv && \
#     /app/venv/bin/pip install --upgrade pip && \
#     /app/venv/bin/pip install -r requirements.txt


# # Копирование конфигурации Nginx
# USER root
# COPY --chown=root:root nginx.conf /etc/nginx/nginx.conf

# # Настройка прав доступа для Nginx
# RUN chmod -R 755 /var/log/nginx /var/cache/nginx /var/run/nginx.pid && \
#     chown -R appuser:appuser /var/log/nginx /var/cache/nginx /var/run/nginx.pid

# USER appuser

# EXPOSE 8000
# EXPOSE 80

# CMD ["/bin/bash", "-c", "supervisord -c /app/supervisord.conf"]


