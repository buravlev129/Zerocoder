# Запуск скриптов инициализации


docker exec -it -w /app Magazin bash -c "sh admin/manage-migrate.sh"

# docker exec -it -w /app -e DJANGO_SUPERUSER_PASSWORD="adm@12345++" Magazin bash -c "sh admin/manage-create-superuser.sh"
docker exec -it -w /app Magazin bash -c "export DJANGO_SUPERUSER_PASSWORD='adm@12345++' && sh admin/manage-create-superuser.sh"

docker exec -it -w /app Magazin bash -c "sh admin/manage-collect-static.sh"
