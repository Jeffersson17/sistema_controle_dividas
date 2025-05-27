echo "starting migrate"
python3 manage.py migrate

echo "starting server"
python manage.py runserver 0.0.0.0:8000