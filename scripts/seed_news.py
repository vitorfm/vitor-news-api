import os
import sys
import django
from django.utils.text import slugify
from django.utils.timezone import now

# Configura Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "vitor_news.settings")
django.setup()

from news.models import News, Category
from django.contrib.auth.models import User

# Lista de notícias
news_list = [
    {
        "title": "Reforma Tributária é Aprovada",
        "subtitle": "Mudanças significativas no sistema fiscal",
        "content": "A nova reforma tributária muda o cenário fiscal do país.",
        "category": "Tributos",
        "status": "published",
        "pro_only": True,
    },
    {
        "title": "Avanços na Vacinação",
        "subtitle": "Saúde pública alcança áreas remotas",
        "content": "Campanhas de vacinação chegam a áreas distantes.",
        "category": "Saúde",
        "status": "draft",
        "pro_only": False,
    },
    {
        "title": "Nova Política Energética Anunciada",
        "subtitle": "Investimento em energia limpa cresce",
        "content": "O governo lança medidas de incentivo à energia solar.",
        "category": "Energia",
        "status": "published",
        "pro_only": True,
    },
    {
        "title": "Mudanças nas Leis Trabalhistas",
        "subtitle": "Flexibilização é foco da nova proposta",
        "content": "Reforma trabalhista busca flexibilizar contratos.",
        "category": "Trabalhista",
        "status": "draft",
        "pro_only": False,
    },
    {
        "title": "CPI do Poder é Instaurada",
        "subtitle": "Investigações sobre uso de verbas públicas",
        "content": "Senadores abrem investigação sobre verbas do orçamento secreto.",
        "category": "Poder",
        "status": "published",
        "pro_only": True,
    },
]

# Popula
for item in news_list:
    category, _ = Category.objects.get_or_create(
        name=item["category"], defaults={"slug": slugify(item["category"])}
    )

    pub_date = now() if item["status"] == "published" else None

    news, created = News.objects.get_or_create(
        title=item["title"],
        defaults={
            "subtitle": item["subtitle"],
            "content": item["content"],
            "category": category,
            "status": item["status"],
            "pro_only": item["pro_only"],
            "author_id": 1,
            "pub_date": pub_date,
            "scheduled_pub_date": pub_date or now(),
        },
    )
    if created:
        print(f"Notícia criada: {news.title}")
    else:
        print(f"Notícia já existia: {news.title}")
