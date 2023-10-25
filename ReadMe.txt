Como rodar o projeto localmente

- Ter as dependencias Python e pip instaladas e configuradas carregatamente

- Ativar o ambiente virtual
.\envPi2\Scripts\activate

- Criar as tabelas do banco de dados
py manage.py makemigrations plataforma

py manage.py migrate

- Popular as tabelas com as informações base
py manage.py loaddata fixtures\cities_states.json

- Finalmente, rodar o projeto
py manage.py runserver