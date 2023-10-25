.\envPi2\Scripts\activate

py manage.py loaddata fixtures\cities_states.json

py manage.py makemigrations plataforma

py manage.py migrate

py manage.py runserver