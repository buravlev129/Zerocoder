#!/bin/bash 


docker run -d -w /app -p 8000:8000 --name FDBot perpetoom/fd-bot:1.0
