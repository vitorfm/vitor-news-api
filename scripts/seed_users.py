import os
import sys
import django

# Adiciona o diretório raiz do projeto ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vitor_news.settings")
django.setup()

from django.contrib.auth.models import User, Group

"""Reseta o banco de dados removendo todos os usuários e grupos"""
print("Resetando usuarios do banco de dados...")
User.objects.all().delete()
Group.objects.all().delete()
print("usuarios resetados com sucesso!")

USERS = [
    {
        "username": "admin",
        "email": "admin@example.com",
        "password": "admin123",
        "is_superuser": True,
        "is_staff": True,
        "groups": [],
    },
    {
        "username": "editor",
        "email": "editor@example.com",
        "password": "editor123",
        "is_superuser": False,
        "is_staff": True,
        "groups": ["Editor"],
    },
    {
        "username": "leitor_info",
        "email": "info@example.com",
        "password": "info123",
        "is_superuser": False,
        "is_staff": False,
        "groups": ["Leitor"],
    },
    {
        "username": "leitor_pro",
        "email": "pro@example.com",
        "password": "pro123",
        "is_superuser": False,
        "is_staff": False,
        "groups": ["Leitor"],
    },
]

for user_data in USERS:
    if not User.objects.filter(username=user_data["username"]).exists():
        user = User.objects.create_user(
            username=user_data["username"],
            email=user_data["email"],
            password=user_data["password"],
        )
        user.set_password(user_data["password"])  # <- força a senha correta
        user.is_superuser = user_data["is_superuser"]
        user.is_staff = user_data["is_staff"]
        user.save()

        for group_name in user_data["groups"]:
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

        print(f"Usuário {user.username} criado com sucesso.")
    else:
        print(f"Usuário {user_data['username']} já existe.")
        user = User.objects.get(username=user_data["username"])
        user.set_password(user_data["password"])  # <- força a senha correta
        user.save()
