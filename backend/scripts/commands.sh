#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT) ..."
  sleep 2
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo "⚙️ Creating superuser admin ..."
python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); user = User.objects.get(username='admin'); user.set_password('159753'); user.save()"

echo "✅ Superuser admin created successfully"

gunicorn --bind 0.0.0.0:8000 --timeout 120 medtrace.wsgi:application