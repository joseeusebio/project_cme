# Project MedTrace

Projeto de gerenciamento de materiais médicos no CME utilizando Django Rest Framework para a API e React para o frontend.

## Configuração do Ambiente

Siga os passos abaixo para configurar e utilizar o sistema.

### Clonar o repositório

1. Clone o repositório:
    ```bash
    git clone https://github.com/joseeusebio/project_medtrace.git
    ```

### Criação de um Virtual Environment

1. Crie e ative um virtual environment:
    ```bash
    python -m venv .venv
    ```
    - Unix ou MacOS:
        ```bash
        source .venv/bin/activate
        ```
    - Windows:
        ```bash
        .venv\Scripts\activate
        ```

### Variáveis de Ambiente

As variáveis de ambiente necessárias já estão disponíveis no repositório no arquivo `.env`.

### Iniciar o Docker para rodar a aplicação

1. Execute o comando abaixo para iniciar os containers Docker:
    ```bash
    docker-compose up --build
    ```

### Inicialização dos Dados

1. Execute o script de inicialização de dados para configurar o ambiente:
    ```bash
    docker exec -it djangoapi python manage.py init_data
    ```

### Credenciais Criadas pelo Script

O script `init_data` cria as seguintes credenciais:

- **Administrador**
  - Usuário: `admin`
  - Senha: `159753`

- **Enfermeiro**
  - Usuário: `enfermeiro`
  - Senha: `123456`
  - Email: `enfermeiro@example.com`

- **Técnico**
  - Usuário: `tecnico`
  - Senha: `123456`
  - Email: `tecnico@example.com`

## Documentação da API

A API utiliza autenticação via JWT para as requisições.

### Acessar a documentação da API

1. Acesse a documentação da API nos seguintes links após iniciar a aplicação:
    - [Swagger](http://localhost:8000/swagger/)
    - [ReDoc](http://localhost:8000/redoc/)

## Telas do Frontend

### Produtos
- Listagem, criação, edição e exclusão de produtos.

### Recebimento de Materiais
- Gestão de lotes de produtos recebidos, incluindo criação, atualização e exclusão de registros.

### Ordem de Tratamento
- Criação e gestão de ordens de tratamento para materiais, incluindo processos de lavagem, esterilização, descarte e distribuição.

### Requisição de Materiais
- Criação e gestão de requisições de materiais para diferentes departamentos, com status de pendente ou concluído.

### Saldo Total de Produtos
- Visualização do saldo total de produtos disponíveis.

### Saldo a Distribuir
- Visualização do saldo de produtos que estão prontos para distribuição.

---

## Contato

Para mais informações, entre em contato pelo email: joseeusebioeng@gmail.com
