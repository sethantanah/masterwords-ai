web: sh -c 'cd ./aitools/ && python manage.py makemigrations && python manage.py migrate && gunicorn aitools.wsgi --threads 3 --timeout 200'