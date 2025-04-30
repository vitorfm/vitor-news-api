from django.apps import AppConfig
from django.db.models.signals import post_migrate
import os


class NewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "news"

    def ready(self):
        post_migrate.connect(create_initial_data, sender=self)


def create_initial_data(sender, **kwargs):
    from django.utils.text import slugify
    from news.models import News, Category
    from django.contrib.auth.models import User, Group
    from django.utils.timezone import now

    if os.environ.get("DJANGO_LOAD_INITIAL_DATA") != "true":
        return  # ⛔ não roda os seeds durante os testes

    if not User.objects.filter(username="admin").exists():
        admin = User.objects.create_superuser("admin", "admin@example.com", "admin123")
        print("✅ Superusuário 'admin' criado")

    editor_group, _ = Group.objects.get_or_create(name="Editor")
    leitor_group, _ = Group.objects.get_or_create(name="Leitor")

    if not User.objects.filter(username="editor").exists():
        editor = User.objects.create_user("editor", "editor@example.com", "editor123")
        editor.groups.add(editor_group)
        print("✅ Usuário 'editor' criado")

    if not User.objects.filter(username="leitor_pro").exists():
        leitor_pro = User.objects.create_user(
            "leitor_pro", "leitor_pro@example.com", "pro123"
        )
        leitor_pro.groups.add(leitor_group)
        print("✅ Usuário 'leitor_pro' criado")

    if not User.objects.filter(username="leitor_info").exists():
        leitor_pro = User.objects.create_user(
            "leitor_info", "leitor_info@example.com", "info123"
        )
        leitor_pro.groups.add(leitor_group)
        print("✅ Usuário 'leitor_info' criado")

    # Categorias
    categories = [
        "Poder",
        "Tributos",
        "Saúde",
        "Energia",
        "Trabalhista",
    ]

    category_objs = {}
    for name in categories:
        slug = slugify(name)
        obj, created = Category.objects.get_or_create(
            name=name, defaults={"slug": slug}
        )
        if not created:
            obj.slug = slug
            obj.save()
            print(f"ℹ️ Categoria já existia: {name} — slug atualizado")
        else:
            print(f"✅ Categoria criada: {name}")
        category_objs[name] = obj

    # Notícias
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

    admin = User.objects.get(username="admin")
    for item in news_list:
        category = category_objs[item["category"]]
        pub_date = now() if item["status"] == "published" else None

        news, created = News.objects.get_or_create(
            title=item["title"],
            defaults={
                "subtitle": item["subtitle"],
                "content": item["content"],
                "category": category,
                "status": item["status"],
                "pro_only": item["pro_only"],
                "author": admin,
                "pub_date": pub_date,
                "scheduled_pub_date": pub_date or now(),
            },
        )
        if created:
            print(f"📰 Notícia criada: {news.title}")
        else:
            print(f"ℹ️ Notícia já existia: {news.title}")
