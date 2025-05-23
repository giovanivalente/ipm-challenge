# IPM Challenge

## 🧠 Visão Geral

Este projeto é uma API REST desenvolvida com Django e Django REST Framework, criada como solução para o desafio técnico da IPM. Ele oferece funcionalidades de autenticação, gerenciamento de contas e predição de saldo futuro com modelo de IA simples.

O modelo de IA do projeto é um modelo simples de regressão linear, treinado para prever o saldo futuro de uma conta bancária com base em dados históricos fornecidos pelo usuário.

---

## 🧩 Funcionalidades

- Registro de novas contas
- Autenticação via JWT
- Consulta, atualização e exclusão de conta autenticada
- Predição de saldo futuro com IA
- Documentação automatizada com Swagger/OpenAPI
- Testes automatizados com pytest e coverage
- Linting com ruff e cobertura com coverage

---

## 🚀 Tecnologias

- **Python** 3.13
- **Django** 5+
- **Django REST Framework**
- **Poetry** para gerenciamento de dependências
- **Docker** + **Docker Compose** para containerização
- **SQLite** como banco de dados local
- **DRF Spectacular** para documentação automática da API
- **Joblib** para salvar o modelo de predição
- **Pytest** para testes automatizados

---

## 📦 Instalação com Docker

### 1. Clone o repositório

```bash
git clone git@github.com:giovanivalente/ipm-challenge.git
cd ipm-challenge
```

### 2. Build da imagem

```bash
docker-compose build
```

### . Subida dos serviços

```bash
docker-compose up
```
⚠️ Ao iniciar, o container executa automaticamente as migrações do Django (python manage.py migrate) e sobe o servidor em http://localhost:8000.

## 📦 Instalação sem Docker

### 1. Clone o repositório

```bash
git clone git@github.com:giovanivalente/ipm-challenge.git
cd ipm-challenge
```

### 2. Instale o Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Adicione o Poetry ao PATH (se necessário):

```bash
export PATH="$HOME/.local/bin:$PATH"
```

### 3. Instale as dependências

```bash
poetry install
```

### 4. Ative o ambiente virtual

```bash
poetry shell
```

### 5. Aplique as migrações

```bash
python manage.py migrate
```

### 6. Inicie o servidor de desenvolvimento

```bash
python manage.py runserver
```

---

## 🧭 Fluxo de uso da API

- ### Criar conta
    Envie nome, email e senha para `/api/v1/account/register/`
- ### Autenticar
    Envie email e senha para /api/v1/login/ e receba um token JWT.
- ### Usar endpoints autenticados
    Use o token recebido no header Authorization: Bearer <access_token> para acessar os recursos de conta e predição.

---

## 📮 Endpoints

### Autenticação

- `POST /api/v1/login/` - Gera um par de tokens JWT (access, refresh) para autenticação.

#### Body
```json
{
    "email": "xispirito@gmail.com",
    "password": "Senha@123"
}
```
#### Response
```json
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl...",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl9..."
}
```

### Contas

- `POST /api/v1/account/register/` - Cria uma nova conta de usuário.

A senha precisa conter:

- Mínimo 8 caracteres
- Uma letra minúscula
- Uma letra maiúscula
- Um caractere especial

#### Body
```json
{
    "name": "Xispirito da Silva",
    "email": "xispirito@gmail.com",
    "password": "Senha@123"
}
```
#### Response
```json
{
    "id": "4844f9bc-4bb8-4725-ae0c-b49eb0ddd77c",
    "name": "Xispirito da Silva",
    "email": "xispirito@gmail.com",
    "is_active": true,
    "created_at": "2025-05-23T14:37:15.138705Z",
    "updated_at": "2025-05-23T14:37:15.138774Z"
}
```

- `GET /api/v1/account/` - Retorna os dados da conta logada **(requer autenticação)**.

#### Response
```json
{
    "id": "4844f9bc-4bb8-4725-ae0c-b49eb0ddd77c",
    "name": "Xispirito da Silva",
    "email": "xispirito@gmail.com",
    "is_active": true,
    "created_at": "2025-05-23T14:37:15.138705Z",
    "updated_at": "2025-05-23T14:37:15.138774Z"
}
```

- `PATCH /api/v1/account/` - Atualiza os dados da conta logada **(requer autenticação)**.

#### Body
```json
{
    "name": "Xispirito da Silva Silva",
    "password": "Password@123",
    "current_password": "Senha@123"
}
```
#### Response
```json
{
    "id": "c9467397-46da-4cf2-9fb5-0db49c1e9244",
    "name": "Xispirito da Silva Silva",
    "email": "xispirito@gmail.com",
    "is_active": true,
    "created_at": "2025-05-23T14:58:28.670215Z",
    "updated_at": "2025-05-23T15:06:14.687943Z"
}
```

- `DELETE /api/v1/account` - Faz uma exclusão da conta logada **(requer autenticação)**.

### Predição

- `POST /api/v1/prediction/balance` - Recebe os dados históricos e prevê o saldo futuro da conta **(requer autenticação)**.

O modelo recebe:

- `avg_deposit`: Média de valores recebidos na conta por mês.
- `avg_withdrawal`: Média de valores sacados da conta por mês.
- `current_balance`: Saldo atual da conta.
- `months_ahead`: Quantidades de meses no futuro que se deseja prever o saldo da conta.

#### Body
```json
{
    "avg_deposit": 923,
    "avg_withdrawal": 437,
    "current_balance": 500,
    "months_ahead": 2
}
```
#### Response
```json
{
    "future_balance": "899.09"
}
```

---

## 📘 Documentação da API

Este projeto utiliza drf-spectacular para gerar documentação automatizada da API no padrão OpenAPI 3.0.

```
http://localhost:8000/api/v1/docs/
http://localhost:8000/api/v1/redoc/
```
---

## ✅ Testes

Este projeto utiliza pytest para execução dos testes automatizados e coverage para geração de relatório de cobertura.

Para rodar os testes com Docker:

```bash
docker-compose exec web task test
```

Para rodar os testes sem Docker:

```bash
task test
```
O comando roda os testes e gera um relatório HTML que pode ser acessado em:

```
http://localhost:63342/ipm-challenge/htmlcov/index.html
```
---

## 🧾 Licença

Este projeto é apenas para fins educacionais/desafio técnico.