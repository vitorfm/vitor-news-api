#!/bin/bash

# Espera o banco de dados estar pronto
echo "Esperando o banco de dados iniciar..."
sleep 5

# Aplica migrações
echo "Aplicando migrações..."
python manage.py migrate

# Coleta arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput

# Cria usuários iniciais (admin, editor e leitor)
echo "Criando usuários iniciais..."
python manage.py shell << END
from django.contrib.auth.models import User, Group

admin_user, created = User.objects.get_or_create(username='admin', defaults={'email': 'admin@example.com'})
if created:
    admin_user.set_password('admin123')
    admin_user.is_superuser = True
    admin_user.is_staff = True
    admin_user.save()

editor_group, _ = Group.objects.get_or_create(name='Editor')
leitor_group, _ = Group.objects.get_or_create(name='Leitor')

editor_user, created = User.objects.get_or_create(username='editor', defaults={'email': 'editor@example.com'})
if created:
    editor_user.set_password('editor123')
    editor_user.save()
    editor_user.groups.add(editor_group)

reader_user, created = User.objects.get_or_create(username='reader', defaults={'email': 'reader@example.com'})
if created:
    reader_user.set_password('reader123')
    reader_user.save()
    reader_user.groups.add(leitor_group)

print("Usuários criados: admin/admin123, editor/editor123, reader/reader123")
END

# Inicia o servidor
echo "Iniciando o servidor..."
gunicorn vitor_news.wsgi:application --bind 0.0.0.0:8000
