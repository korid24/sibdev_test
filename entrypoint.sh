echo "Waiting for Postgres"
while ! nc -z "db" "5432"; do
  echo "sleep"
  sleep 1
done
echo "Postgres started"

python manage.py migrate
python manage.py collectstatic --no-input --clear

exec "$@"
