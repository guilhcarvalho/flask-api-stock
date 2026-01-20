# Flask API – Controle de Estoque

API REST desenvolvida com Flask para gerenciamento de estoque, com autenticação de usuários e controle de permissões.

## Tecnologias utilizadas

- **Python 3.11.9**
- **Poetry** - Gerenciador de pacotes.
- **Flask** - Framework.
- **Flask-SQLAlchemy** - Responsável pelo ORM.
- **Flask-JWT-Extended** - Criação de JSON Web Tokens para autenticação de usuários.
- **Flask-bcrypt** - Criptografia das senhas dos usuários.
- **Flask-Marshmallow** - Serialização e deserialização de JSON.
- **apispec-webframeworks** - Documentação Swagger
- **SQLite** - Banco de dados

## Funcionalidades

- Cadastro e autenticação de usuários
- Autorização por permissões/roles
- CRUD de itens do estoque
- Validação de dados
- API REST seguindo padrões HTTP

## Estrutura do projeto

O projeto se baseia na arquitetura **MVC (Models, Views e Controllers)** com a adição da camada **Services**.

- **Models** - Camada para os modelos de tabelas do banco de dados.
- **Views** - Camada de serialização e deserialização de JSON.
- **Controllers** - Camada de execução das rotas.
- **Services** - Camada com algumas regras de negócios.

## Executando o projeto

Após clonar o repositório é necessário:
- Ter o python na versão **3.11.9**.
- Software Insomnia ou similar para fazer as requisições.
- Dependências do projeto

Executar o comando no terminal para executar o servidor(Flask)

```bash
ENVIRONMENT=development poetry run flask --app src.app run --debug
```

Poetry é o responsável pelo ambiente virtual e gerenciador de pacotes e ENVIRONMENT=development define a variável de desenvolvimento no arquivo config.py que configura cada ambiente.