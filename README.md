Vitor News API
API RESTful para gestão de notícias, com autenticação JWT, controle de acesso por perfil de usuário, agendamento de publicações e documentação via Swagger.

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

📰 Funcionalidades Principais
1. CRUD de notícias
2. Upload de imagens
3. Controle de publicação (imediata e agendada)
4. Diferentes perfis de usuário (Admin, Editor, Leitor)
5. Controle de acesso por plano PRO/INFO
6. Documentação automática via Swagger

📚 Documentação da API
. Swagger UI: http://127.0.0.1:8000/swagger/
. Redoc: http://127.0.0.1:8000/redoc/

🛠️ Tecnologias Utilizadas
. Django
. Django REST Framework
. SimpleJWT
. drf-yasg (Swagger)
. Pillow
. PostgreSQL ou SQLite (desenvolvimento)

⚠️ Aviso
Este projeto foi desenvolvido exclusivamente para fins do proprietário.
O uso, reprodução ou redistribuição sem autorização é expressamente proibido enquanto o repositório for privado.
Após tornado público, estará sob os termos da licença MIT.