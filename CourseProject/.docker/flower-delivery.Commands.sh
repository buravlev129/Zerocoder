

docker run -d --name Magazine -p 8000:8000  perpetoom/backend/flower-delivery:1.0 tail -f /dev/null
docker exec -it Magazine python3 --version

docker exec -it -w /app Magazine bash



