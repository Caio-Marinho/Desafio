# Deafio de Back-end

## Situação-Problema
Uma startup chamada "BookBridge" está desenvolvendo uma plataforma que facilita a criação e o gerenciamento de clubes de leitura online. 
O objetivo é permitir que grupos de pessoas se reúnam para discutir livros, planejem sessões de leitura e compartilhem suas impressões. 
Eles precisam de uma API que permita que os usuários se cadastrem, 
criem clubes de leitura, adicionem livros à lista de leitura do clube e registrem suas opiniões sobre os livros lidos. 
A API deve oferecer um sistema de autenticação para garantir a segurança dos dados dos usuários e fornecer estatísticas básicas sobre as leituras.

### Features Obrigatórias:

1. CRUD de usuários e clubes de leitura.

2. Endpoint para adicionar e gerenciar a lista de livros dos clubes.

3. Implementação de autenticação com JWT.

4. Persistência de dados em banco de dados SQL.

5. Endpoint para registrar opiniões e avaliações dos livros lidos.

### Features Não Obrigatórias:

1. Implementação de um sistema de cache para melhorar a performance.

2. Implementação de testes unitários.

3. Endpoint adicional que forneça estatísticas como o número médio de livros lidos por clube ou a média de avaliações dos livros.

4. Registro de logs de atividades na API.

## Estrutura de Pastas
```
/app
|---/auth - Pasta referente aos arquivos de autenticação
|---/config - Pasta referente aos arquivos de Configuração do Sistema(Ex.: Conexão com o banco de dados)
|---/models - Pasta referente aos arquivos e modelos do banco de dados
|---/log - Pasta referente aos arquivos de log
```
## Estrutura de Arquivos
```
/app
 -- app.py - Arquivo principal que está executando todo o sistema
```
```
/auth
  -- __init__.py - Arquivo que inicializa a exetenção do flask_jwt_extended
  -- auth.py - Arquivo responsável pela autenticação
```
```
/config
 -- config.py - Arquivo de configuração do sistema
```
```
/log
  --logger.py - Arquivo que controla o log do sistema e cria o arquivo Acess.log
  -- Acess.log - Arquivo por registra todos eventos que o sistema vivência
```
```
/models
 -- __init__.py - Arquivo que inicializa a exetenção do flask_sqlalchemy
 -- models.py - Arquivo com o modelo de banco de dados
```

## Back-end 
### Python 
![PYTHON](https://img.shields.io/badge/-PYTHON-black?logo=python&style=social) 
- **Uso**: Linguagem de programação utilizada para desenvolver toda a lógica da aplicação.
- **Versão**: [Python 3.13.0](https://www.python.org/downloads/release/python-3130/)
## Framework 
### Flask 
![FLASK](https://img.shields.io/badge/-FLASK-black?logo=flask&style=social) 
- **Uso**: Framework web micro utilizado para construir a API do projeto.

#### Flask-SQLAlchemy 
![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-black?logo=SQLAlchemy&style=social) 
- **Uso**: Extensão do Flask que fornece uma interface ORM (Object-Relational Mapping) para interagir com bancos de dados SQL de maneira mais intuitiva e eficiente.

#### Flask-JWT-Extended 
![JWT](https://img.shields.io/badge/-JWT-black?logo=JSONWebTokens&style=social) 
- **Uso**: Extensão que facilita a implementação de autenticação JWT (JSON Web Tokens) em aplicações Flask.

#### Flask-Caching 
![Caching](https://img.shields.io/badge/-Caching-black?logo=Cache&style=social)
- **Uso**: Extensão para adicionar funcionalidades de cache à aplicação Flask. Foi utilizada para melhorar a performance da aplicação armazenando temporariamente dados frequentemente acessados, reduzindo a necessidade de consultas repetidas ao banco de dados.

## Database 
### MySQL 
![MYSQL](https://img.shields.io/badge/-MYSQL-black?logo=mysql&style=social) 
- **Uso**: Sistema de gerenciamento de banco de dados relacional utilizado para armazenar dados persistentes da aplicação, como informações de usuários, clubes de leitura

## Ferramentas

### PyCharm
![PyCharm](https://img.shields.io/badge/-PyCharm-black?logo=PyCharm&style=social)
- **Uso**: Ambiente de desenvolvimento integrado (IDE) utilizado para escrever e depurar o código Python.

### Postman
![Postman](https://img.shields.io/badge/-Postman-black?logo=Postman&style=social)
- **Uso**: Ferramenta para testar e documentar a API. Utilizada para enviar requisições HTTP, verificar respostas e garantir que os endpoints da API estejam funcionando corretamente.

### Redis
![Redis](https://img.shields.io/badge/-Redis-black?logo=Redis&style=social)
- **Uso**: Utilizado como sistema de cache para melhorar a performance da aplicação. Armazena temporariamente dados frequentemente acessados, reduzindo a carga no banco de dados SQL.