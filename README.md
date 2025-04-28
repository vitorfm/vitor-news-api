# Vitor News API 📳

![Build Status](https://github.com/vitorfm/vitor-news-api/actions/workflows/ci.yml/badge.svg)


API RESTful para gestão de notícias, com autenticação JWT, controle de acesso por perfil de usuário, agendamento de publicações, processamento assíncrono com Celery e Redis, documentação via Swagger e pipeline de Integração Contínua com GitHub Actions.

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
- Categorias de notícias por verticais (Poder, Tributos, Saúde, Energia, Trabalhista)
- Envio de e-mails de notificação (assíncrono via Celery)
- Agendamento de tarefas futuras com Celery Beat
- Testes automatizados de funcionalidades críticas
- Integração Contínua com GitHub Actions

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

- Use o **access token** no botão **Authorize** do Swagger para autenticar nas rotas protegidas.

---

## 📚 Documentação da API

- [Swagger UI](http://127.0.0.1:8000/swagger/)
- [Redoc](http://127.0.0.1:8000/redoc/)

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

## ⚠️ Aviso

Este projeto foi desenvolvido exclusivamente para fins do proprietário.  
O uso, reprodução ou redistribuição sem autorização é expressamente proibido enquanto o repositório for privado.  
Após tornado público, estará sob os termos da licença MIT.