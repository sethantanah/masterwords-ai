web: sh -c 'cd ./aitools/ && python manage.py makemigrations && python manage.py migrate && gunicorn aitools.wsgi --treads 3 ---timeout 200'