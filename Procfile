release: python manage.py migrate
web: gunicorn CMW.wsgi --log-file -
heroku ps:scale web
