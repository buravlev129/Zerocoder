#!/bin/bash

mkdir -p container/{admin,logs,storage}

# Если папка admin пустая, копируем скрипты из временного контейнера
if [ -z "$(ls -A container/admin)" ]; then
    docker run --rm -v ${PWD}/container/admin:/target perpetoom/flower-delivery:1.0 \
           bash -c "cp -r /app/admin/* /target/"
fi

# Запускаем основной контейнер
docker run -d -p 8000:8000 \
           -v ${PWD}/container/admin:/app/admin \
           -v ${PWD}/container/logs:/app/logs \
           -v ${PWD}/container/storage:/app/storage \
           --name Magazin perpetoom/flower-delivery:1.0



