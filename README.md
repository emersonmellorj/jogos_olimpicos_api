# API para o Desafio COB - Jogos Olímpicos

Seguem abaixo as orientações e informações sobre o desenvolvimento da API para os Jogos Olímpicos.

Para o desenvolvimento da solução foram utilizadas as bibliotecas da linguagem Python3:

certifi==2020.4.5.1
chardet==3.0.4
Django==2.2.9
django-filter==2.2.0
django-redis==4.11.0
djangorestframework==3.11.0
Faker==4.0.3
idna==2.9
importlib-metadata==1.6.0
Markdown==3.2.1
more-itertools==8.2.0
packaging==20.3
pluggy==0.13.1
py==1.8.1
pyparsing==2.4.7
pytest==5.4.1
python-dateutil==2.8.1
pytz==2019.3
redis==3.4.1
requests==2.23.0
six==1.14.0
sqlparse==0.3.1
text-unidecode==1.3
urllib3==1.25.9
wcwidth==0.1.9
zipp==3.1.0

Obs: Como não publiquei a API, utilizei apenas o servidor de desenvolvimento do Django.

Em relação aos testes automáticos, utilizei a biblioteca Pytest para desenvolver as classes e métodos de testes. Não fiz o uso da biblioteca UNITTEST.

Em relação ao Django Rest Framework, utilizei alguns recursos importantes como:

- Throttling (controle de requisições para usuários anônimos e cadastrados);
- Cache das requisições no Redis (configurei apenas 1 minuto de cache a nível de testes);
- Acesso a API com autenticação por Token;
- Resultados paginados a cada 10 registros.

Utilizei também o recurso Router para a criação automática de rotas da API, conforme a criação das Views. Estas foram desenvolvidas baseadas em viewsets.

Temos os métodos GET, POST, PUT e DELETE para a maioria dos endpoints. Para o endpoint do Ranking das Etapas de cada categoria temos apenas o método GET disponível.

Estes foram os endpoints criados:

- http://localhost:8000/api/v1/stage/
- http://localhost:8000/api/v1/stage/2/
- http://localhost:8000/api/v1/modality/
- http://localhost:8000/api/v1/modality/3/

Ira retornar os dados da modalidade escolhida bem como os atletas desta modalidade + as etapas criadas para esta modalidade.
Para verificar / atualizar / excluir uma modalidade especifica:
http://localhost:8000/api/v1/modality/3/

http://localhost:8000/api/v1/athletes/
http://localhost:8000/api/v1/athletes/1/

http://localhost:8000/api/v1/modality/3/athletes/

http://localhost:8000/api/v1/results/
http://localhost:8000/api/v1/results/5/

http://localhost:8000/api/v1/stage/2/ranking/


Seguem abaixo algumas regras da API:

