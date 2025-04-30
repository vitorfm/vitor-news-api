import os
import sys
import django
from django.utils.text import slugify

# Adiciona o diretório raiz do projeto ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vitor_news.settings")
django.setup()

# Agora sim: importa os modelos
from news.models import Category

# Lista de categorias
categories = [
    "Poder",
    "Tributos",
    "Saúde",
    "Energia",
    "Trabalhista",
]

# Criação ou atualização das categorias
for name in categories:
    slug = slugify(name)
    obj, created = Category.objects.get_or_create(name=name, defaults={"slug": slug})
    if not created:
        obj.slug = slug
        obj.save()
        print(f"Categoria já existia: {name} — slug atualizado")
    else:
        print(f"Categoria criada: {name}")
