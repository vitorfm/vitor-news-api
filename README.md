Vitor News API 📳

API RESTful para gestão de notícias, com autenticação JWT, controle de acesso por perfil de usuário, agendamento de publicações, processamento assíncrono com Celery e Redis, e documentação via Swagger.

📰 Funcionalidades Principais
1. CRUD completo de notícias
2. Upload de imagens
3. Controle de publicação (imediata e agendada)
4. Diferentes perfis de acesso (Admin, Editor, Leitor)
  . Admin: gerenciamento completo
  . Editor: gerencia apenas suas próprias notícias
  . Leitor: acessa apenas notícias públicas ou conforme plano contratado
5. Controle de acesso por plano PRO/INFO
6. Autenticação JWT
7. Documentação automática via Swagger
8. Categorias de notícias por verticais (Poder, Tributos, Saúde, Energia, Trabalhista)
9. Envio de e-mails de notificação (assíncrono via Celery)
10. Agendamento de tarefas futuras
11. Testes automatizados de funcionalidades críticas
12. Celery Beat para agendar a publicação automática de notícias que possuem uma data e hora de agendamento

🚀 Como Rodar o Projeto

1. Clone o repositório:

git clone https://github.com/vitorfm/vitor-news-api.git
cd vitor-news-api

2. Crie e ative o ambiente virtual:

python3 -m venv venv
source venv/bin/activate  # (Mac/Linux)
venv\Scripts\activate     # (Windows)

3. Instale as dependências:

pip install -r requirements.txt

4. Realize as migrações:

python3 manage.py makemigrations
python3 manage.py migrate

5. Crie um superusuário:

python3 manage.py createsuperuser

6. Rode o servidor local:

python3 manage.py runserver


🔐 Autenticação

. Gere o token JWT via:

POST /api/token/
Exemplo de corpo:

{
  "username": "seu_usuario",
  "password": "sua_senha"
}

. Use o access token no botão Authorize do Swagger para autenticar.



📚 Documentação da API
. Swagger UI: http://127.0.0.1:8000/swagger/
. Redoc: http://127.0.0.1:8000/redoc/

🛠️ Tecnologias Utilizadas
. Python 3.13
. Django 4.2
. Django REST Framework
. SimpleJWT
. drf-yasg (Swagger)
. Redis (como broker do Celery)
. Celery 
. Pillow
. PostgreSQL ou SQLite (desenvolvimento)

📬 Rodar o Celery e o Redis

. Certifique-se que o Redis esteja rodando na sua máquina.
. Para iniciar o worker do Celery:
    celery -A vitor_news worker --loglevel=info

. Todas as tarefas assíncronas (como envio de e-mails) serão processadas no background pelo Celery.

🧪 Rodar Testes

. Para rodar todos os testes automatizados:
  python3 manage.py test

. Os testes cobrem:
  1. Criação de notícias
  2. Publicação de notícias
  3. Controle de acesso por perfil
  4. Restrições de leitura para leitores

  
  ---

## 🔄 Publicação Automática de Notícias

O sistema utiliza o **Celery Beat** para agendar a publicação automática de notícias que possuem uma data e hora de agendamento (`scheduled_pub_date`).

- A cada 1 minuto, o Celery Beat dispara a execução da tarefa `publish_scheduled_news`.
- A tarefa consulta todas as notícias que:
  - Estão com o status `draft`
  - Têm a `scheduled_pub_date` menor ou igual ao horário atual
- As notícias encontradas são automaticamente publicadas.

### Como funciona:

- O **Celery Beat** é configurado para usar o banco de dados do Django como fonte de agendamento, via `django_celery_beat`.
- O agendamento é gerenciado diretamente pelo Django Admin, na seção de "Periodic Tasks".

# Terminal 1 - Django server
`python3 manage.py runserver`

# Terminal 2 - Celery Worker
`celery -A vitor_news worker --loglevel=info`

# Terminal 3 - Celery Beat
celery -A vitor_news beat --loglevel=info

  
  🗂️ Estrutura de Pastas
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

⚠️ Aviso
Este projeto foi desenvolvido exclusivamente para fins do proprietário.
O uso, reprodução ou redistribuição sem autorização é expressamente proibido enquanto o repositório for privado.
Após tornado público, estará sob os termos da licença MIT.