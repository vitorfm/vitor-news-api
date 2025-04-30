import os
import sys
import django

sys.path.append("/app")  # garante que o diretório do projeto está no path
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vitor_news.settings")
django.setup()

from django.contrib.auth.models import User, Group

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
        user.is_superuser = user_data["is_superuser"]
        user.is_staff = user_data["is_staff"]
        user.save()

        for group_name in user_data["groups"]:
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

        print(f"Usuário {user.username} criado com sucesso.")
    else:
        print(f"Usuário {user_data['username']} já existe.")
