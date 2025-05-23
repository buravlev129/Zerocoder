#!/bin/bash

docker run -d -p 8000:8000 \
           -v ${PWD}/container/admin:/app/admin \
           -v ${PWD}/container/logs:/app/logs \
           -v ${PWD}/container/storage:/app/storage \
           --name Magazin perpetoom/flower-delivery:1.0 
