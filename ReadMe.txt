Como rodar o projeto localmente

- Ter as dependencias Python (3.12.0) e pip instaladas e configuradas carregatamente

- Ativar o ambiente virtual
.\envPi2\Scripts\activate

- Va para a pasta plataforma-troca-api
   cd plataforma-troca-api

- Criar as tabelas do banco de dados
py manage.py makemigrations plataforma

py manage.py migrate

- Popular as tabelas com as informações base
py manage.py loaddata fixtures\cities_states.json

- Finalmente, rodar o projeto
py manage.py runserver