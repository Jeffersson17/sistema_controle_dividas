# Sistema de Controle de Dívidas (Backend)

Este projeto foi desenvolvido como parte de uma **atividade de extensão da Faculdade Descomplica**. Ele representa o backend de um sistema para controle de dívidas, construído com **Django**, **Django REST Framework**, autenticação via **JWT (SimpleJWT)** e containerizado com **Docker**.

## 📦 Tecnologias Utilizadas

- Python 3.12
- Django
- Django REST Framework
- SimpleJWT
- PostgreSQL
- Docker & Docker Compose

## ⚙️ Funcionalidades

- Cadastro de clientes
- Registro de dívidas
- Histórico de alterações de dívida
- Autenticação com tokens JWT
- API RESTful

## 🚀 Instalação

### Pré-requisitos

- Docker
- Docker Compose

### Passos

1. Clone o repositório:
   ```bash
   git clone https://github.com/Jeffersson17/sistema_controle_dividas.git
   cd sistema-controle-dividas

2. Inicie o projeto:
    ```bash
    docker-compose up --build

## 🔐 Autenticação

Este projeto usa o pacote `SimpleJWT` para autenticação baseada em tokens JWT.

### Endpoints

- `POST /token/` — obtém o par de tokens (access e refresh)
- `POST /token/refresh/` — renova o token de acesso com o refresh token

## 🗃️ Estrutura do Projeto

.
├── django/
│   ├── client/
│   │   ├── migrations/
│   │   ├── tests/
│   │   │   └── test_views.py # Teste unitário das Views
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py # Modelos: Client e Historical
│   │   ├── serializers.py
│   │   └── views.py # Views da API
│   ├── debt_control/
│   │   ├──requirements/
│   │   │    └──main.txt # Requisitos que serão instalados ao iniciar o container
│   │   ├── settings.py
│   │   ├── urls.py # Todas as rotas do projeto
│   │   ├── asgi.py
│   │   └── wsgi.py
│   ├── docker/
│       └── build.sh # Executa migrate + runserver ao iniciar o container
│   ├── Dockerfile
│   └── manage.py
├── envs/
│   └── postgres.env # Variáveis de ambiente do PostgreSQL
├── docker-compose.yml
└── .gitignore
