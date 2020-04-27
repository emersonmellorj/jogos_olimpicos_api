# API para o Desafio COB - Jogos Olímpicos

Seguem abaixo as orientações e informações sobre o desenvolvimento da API para os Jogos Olímpicos.

Para o desenvolvimento da solução foram utilizadas as bibliotecas da linguagem Python 3:

```
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
```
A versão do Python utilizada foi a 3.7 e o banco SQLite.

Obs: Como não publiquei a API, utilizei apenas o servidor de desenvolvimento do Django.

Toda a API foi desenvolvida em um ambiente virtual, sendo inclusive instaladas estas bibliotecas dentro do mesmo.

Não retirei a SECRET_KEY do arquivo settings devido a não ter publicado a aplicação.

Para que a API seja colocada em funcionamento, é necessário a instalação do Redis no servidor. Após a instalação o mesmo deve estar sendo executado.


## Testes Automatizados:

Em relação aos testes automatizados, utilizei a biblioteca Pytest para desenvolver as classes e métodos de testes. Não fiz o uso da biblioteca UNITTEST.


## Versionamento do código:

Foi utilizado o git para versionar cada alteração quer era realizada nos códigos da API.


## DRF e recursos:

Em relação ao Django Rest Framework, utilizei alguns recursos importantes como:

- Throttling (controle de requisições para usuários anônimos e cadastrados);
- Cache das requisições no Redis (configurei apenas 1 minuto de cache a nível de testes). Coloquei apenas algumas views para cachear os resultados;
- Acesso a API com autenticação por Token;
- Resultados paginados a cada 10 registros.

Utilizei também o recurso Router para a criação automática de rotas da API, conforme a criação das Views. Estas foram desenvolvidas baseadas em viewsets.


# Métodos pelos quais a API responde:

Temos os métodos GET, POST, PUT e DELETE para a maioria dos endpoints. Para o endpoint do Ranking das Etapas de cada categoria temos apenas o método GET disponível.


## Lógica de funcionamento da API:

Para nivelarmos o entendimento da lógica da API, temos os seguintes Modelos de Dados:

- Modalidade (Modality): São as modalidades dos jogos.
Ex:. 100m Rasos e Lançamento de Dardos

- Etapa (Stage): São as etapas de cada modalidade.
Ex.: Classificatória 1 que pertence a 100m Rasos;
     Classificatória 1 que pertence a Lançamento de Dardos.
     
- Atleta (Athlete): Cadastro dos atletas das competições.
Ex.: João Brasil que está inscrito na modalidade 100m Rasos.

- Resultados (Results): É aonde cadastramos os resultados dos atletas. Conforme especificado no documento inicial da demanda,  poderá ser cadastrado apenas um resultado para a modalidade 100m Rasos por etapa para cada atleta e 3 resultados para a modalidade Lançamento de Dardos por etapa para cada atleta.

- Ranking: A qualquer momento poderá ser visualizado o ranking das etapas de cada competição.


## Endpoints da API:

Estes foram os endpoints criados:

### Stage (Etapa):

GET / POST:
- http://localhost:8000/api/v1/stage/

PUT / DELETE:
- http://localhost:8000/api/v1/stage/{pk}/

Obs: Para finalizar uma etapa, basta realizer um put no stage desejado, alterando a flag status == False. Quando uma etapa é criada, este campo recebe o valor True.


### Modalidade (Modality):

GET / POST:
- http://localhost:8000/api/v1/modality/

PUT / DELETE:
- http://localhost:8000/api/v1/modality/{pk}/

Ira retornar os dados da modalidade escolhida bem como os atletas desta modalidade + as etapas criadas para esta modalidade.


### Atletas (Athletes):

GET / POST:
http://localhost:8000/api/v1/athletes/
http://localhost:8000/api/v1/modality/{modality_pk}/athletes/

Através deste endpoint acima será possível verificar todos os atletas cadastrados para uma determinada modalidade.

PUT / DELETE:
http://localhost:8000/api/v1/athletes/{pk}/


### Resultados (Results):

GET / POST:
http://localhost:8000/api/v1/results/

PUT / DELETE:
http://localhost:8000/api/v1/results/{pk}/


### Ranking:

GET / LIST
http://localhost:8000/api/v1/stage/{stage_pk}/ranking/

Para visualializar o Ranking de uma etapa específica de uma competição, basta colocar em <stage_pk> o código da etapa que foi cadastrada no banco.


## Regras de funcionamento da API:

Seguem abaixo algumas regras da API:

- Somente será permitido cadastrar um resultado para um atleta se o mesmo pertencer à modalidade no qual 
esta sendo cadastrada. Caso contrário o usuario receberá uma mensagem de erro.

- Somente será permitido cadastrar um resultado se a etapa ainda não foi finalizada.

- Somente será permitido cadastrar um resultado se a etapa escolhida estiver registrada para a competição escolhida.
```
Ex:
Modalidade: 100m rasos
Etapa: Lançamento de Dardo - Classificatoria 1

Isto não será permitido.

Modalidade: 100m rasos
Etapa: 100m rasos - Classificatoria 1

Isto será permitido.
```

- As regras para o numero de cadastro de resultados por Modalidade / Etapa e Atleta são:
    Na competição de 100m Rasos, apenas será permitido o cadastro de um resultado por Modalidade / Etapa para cada atleta.

    Na competição de Lançamento de Dardos, será permitido o cadastro de 3 resultados por Modalidade / Etapa para cada atleta. Fora isso, será retornada uma mensagem de erro informando ao usuário que não é mais possível cadastrar resultados para o atleta. Apenas o melhor resultado aparecerá no Ranking da Etapa.

- Um usuário anônimo só terá direito a 10 requisições por minutos na API. O usuário registrado terá direito a 100 requisçoes por segundo (regras definidas apenas a nível de testes, sem levar em consideração a capacidade do recurso que iria receber esta API).


**_OBS:_** Devido ao cache das requisicoes que sao feitas na API no Redis, será preciso aguardar 1 minuto para validar as operaçoes via consultas na API. Se quiser ter a visualização em tempo real, os objetos deverão ser consultados pelo Django Admin.

**_OBS2:_**: Vale a pena lembrar que, para que as requisições sejam feitas com sucesso, cada usuário deverá ter o seu token gerado, seja pelo Django Admin ou pelo Shel do manage.py. Usuários anônimos estão limitados apenas a consultas.

