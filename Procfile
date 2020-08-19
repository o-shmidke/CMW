release: python manage.py migrate
config:set DISABLE_COLLECTSTATIC=1
web: gunicorn CMW.wsgi --log-file -
heroku ps:scale web
