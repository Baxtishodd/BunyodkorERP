

web: bash -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn dcrm.wsgi:application --bind 0.0.0.0:$PORT"

