echo "*** Startup.sh ***"
echo "Run Migrations:"
python manage.py migrate
echo "Start gunicorn:"
gunicorn --bind=0.0.0.0 --timeout 60 --max-requests 500 --max-requests-jitter 10  _esi_account_management.wsgi --workers=3
