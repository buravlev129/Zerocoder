
python="venv/bin/python"
manage="FlowerDelivery/manage.py"
username="admin"
email="admin@bla-bla.com"

: "${DJANGO_SUPERUSER_PASSWORD:?Не установлена переменная DJANGO_SUPERUSER_PASSWORD}"

# DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD} echo "$python $manage --username $username --email $email PWD=$DJANGO_SUPERUSER_PASSWORD --noinput"
DJANGO_SUPERUSER_PASSWORD=${DJANGO_SUPERUSER_PASSWORD} $python $manage createsuperuser --username $username --email $email --noinput
