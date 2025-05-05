
# Vitor News API 📳

![Build](https://github.com/vitorfm/vitor-news-api/actions/workflows/ci.yml/badge.svg)
![License](https://img.shields.io/github/license/vitorfm/vitor-news-api)

API RESTful para gestão de notícias, com autenticação JWT, controle de acesso por perfil de usuário, agendamento de publicações, processamento assíncrono com Celery e Redis, documentação via Swagger e pipeline de Integração Contínua com GitHub Actions.

---

## ✅ Como testar em 1 minuto (sem instalar nada)

Você pode clonar, rodar com Docker e acessar o Swagger para navegar na API:

```bash
git clone https://github.com/vitorfm/vitor-news-api.git
cd vitor-news-api
cp .env.example .env
docker compose up --build
```

Acesse localmente: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)  

Acesse em produção (Render):

- Documentação Swagger: [https://vitor-news-api.onrender.com/swagger/](https://vitor-news-api.onrender.com/swagger/)
- Redoc: [https://vitor-news-api.onrender.com/redoc/](https://vitor-news-api.onrender.com/redoc/)
- Endpoint principal: [https://vitor-news-api.onrender.com/api/news/](https://vitor-news-api.onrender.com/api/news/)

- Usuário Admin: `admin` • Senha: `admin123`

- Usuário Editor: `editor` Senha: `editor123`

- Usuário Leitor INFO: `leitor_info` Senha: `info123`

- Usuário Leitor PRO: `leitor_pro` Senha: `pro123`

---

## 📰 Funcionalidades Principais

- CRUD completo de notícias
- Upload de imagens
- Controle de publicação (imediata e agendada)
- Diferentes perfis de acesso:
  - **Admin**: gerenciamento completo
  - **Editor**: gerencia apenas suas próprias notícias
  - **Leitor**: acessa apenas notícias públicas ou conforme plano contratado
- Controle de acesso por plano PRO/INFO
- Autenticação JWT
- Documentação automática via Swagger
- Categorias por verticais (Poder, Tributos, Saúde, Energia, Trabalhista)
- Envio de e-mails de notificação (assíncrono via Celery)
- Agendamento de tarefas com Celery Beat
- Testes automatizados
- CI com GitHub Actions
- CD Render integrado com GitHub 

---

## 🐳 Rodar com Docker

```bash
docker compose up --build
```

Isso executa:

- Django + Gunicorn
- PostgreSQL
- Celery Worker
- Celery Beat

Acesse a API em: [http://localhost:8000/swagger/](http://localhost:8000/swagger/)

---

## 🔐 Autenticação JWT

Obtenha o token via:

```http
POST /api/token/
```

Corpo:

```json
{
  "username": "admin",
  "password": "admin123"
}
```

Use o token no botão **Authorize** do Swagger para autenticar.
No campo "value" coloque "Bearer "+"a chave access gerada para o usuário"    

---

## 📬 Publicação Agendada

A cada minuto, o Celery Beat verifica se há notícias com:

- `status="draft"`
- `scheduled_pub_date <= agora`

E publica automaticamente.

Agendamentos são controlados no Django Admin via **Periodic Tasks**.

---

## 🧪 Testes

```bash
python3 manage.py test news.tests
```

Cobertura:
- Criação e publicação de notícias
- Controle de perfis e permissões
- Restrições de leitura conforme plano
- Agendamento e publicação automática

---

## 🔄 CI com GitHub Actions

Ao dar push ou PR:

- Ambiente virtual criado
- Dependências instaladas
- Testes executados

Arquivo: `.github/workflows/ci.yml`

---

## 🗂️ Estrutura de Pastas

```
vitor_news_api/
  news/
    models.py
    views.py
    serializers.py
    permissions.py
    tasks.py
    tests/
  vitor_news/
    settings.py
    urls.py
    celery.py
  manage.py
```

---

## 🎯 Destaques Técnicos

- ✅ Autenticação JWT com controle de perfis
- ✅ Agendamento com Celery + Redis + Beat
- ✅ CI com GitHub Actions
- ✅ Dockerfile e docker-compose
- ✅ Criação automática de usuários padrão
- ✅ Deploy funcionando no Render

---

## 🛠️ Tecnologias Utilizadas

- Python 3.13
- Django 4.2
- Django REST Framework
- SimpleJWT
- drf-yasg (Swagger)
- Redis (como broker do Celery)
- Celery
- Celery Beat (agendador de tarefas)
- PostgreSQL ou SQLite (desenvolvimento)
- GitHub Actions (CI)
- Docker

---

## 🤝 Contribuição

Este projeto foi desenvolvido como parte de um desafio técnico.  
Fico à disposição para apresentar o funcionamento e discutir melhorias.  
Obrigado pela oportunidade 🙏

---

## ⚠️ Licença

Distribuído sob a Licença MIT.

---

## 🚀 Como Rodar o Projeto 

### 1. Clone o repositório

```bash
git clone https://github.com/vitorfm/vitor-news-api.git
cd vitor-news-api
```

### 2. Crie e ative o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # (Mac/Linux)
venv\Scripts\activate     # (Windows)
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Realize as migrações

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### 5. Crie um superusuário

```bash
python3 manage.py createsuperuser
```

### 6. Rode o servidor local

```bash
python3 manage.py runserver
```

---

## 🔐 Autenticação

- Gere o token JWT via:

```http
POST /api/token/
```

Exemplo de corpo:

```json
{
  "username": "seu_usuario",
  "password": "sua_senha"
}
```

---

- Use o **access token** no botão **Authorize** do Swagger para autenticar nas rotas protegidas.

---

## 📬 Rodar o Celery e o Redis

Certifique-se que o Redis esteja rodando localmente.

### Terminal 1 - Django server


```bash
python3 manage.py runserver
```

### Terminal 2 - Celery Worker

```bash
celery -A vitor_news worker --loglevel=info
```

### Terminal 3 - Celery Beat

```bash
celery -A vitor_news beat --loglevel=info
```

---

## 🔄 Publicação Automática de Notícias

O sistema utiliza o **Celery Beat** para agendar a publicação automática de notícias que possuem uma data e hora de agendamento (`scheduled_pub_date`).

- A cada 1 minuto, o Celery Beat dispara a execução da task `publish_scheduled_news`.
- A task publica automaticamente notícias que:
  - Estão com status `draft`
  - Têm `scheduled_pub_date` menor ou igual ao horário atual.

### Como Funciona

- O Celery Beat é configurado para usar o banco de dados do Django como fonte de agendamento (via `django_celery_beat`).
- O agendamento é gerenciado pelo Django Admin em **Periodic Tasks**.

---

## 🧪 Rodar Testes

Execute:

```bash
python3 manage.py test news.tests
```

Os testes cobrem:

- Criação de notícias
- Publicação de notícias
- Controle de acesso por perfil
- Restrições de leitura conforme plano contratado

---

## 🔄 Integração Contínua (CI)

O projeto utiliza **GitHub Actions** para integração contínua:

- Em cada `push` ou `pull request`, o GitHub:
  - Instala o ambiente
  - Instala as dependências
  - Executa migrações
  - Roda os testes automatizados

Workflow YAML usado:  
`.github/workflows/ci.yml`

✅ Assim garantimos qualidade contínua do código.

---

