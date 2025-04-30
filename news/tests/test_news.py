from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from django.utils import timezone
from news.models import Category, News, Subscription
from news.tasks import publish_scheduled_news  # ⬅️ importa a task para testar


class NewsTests(APITestCase):
    def setUp(self):
        # Cria usuários
        self.editor_user = User.objects.create_user(
            username="editor_test", password="senha123"
        )
        self.reader_user = User.objects.create_user(
            username="leitor_test", password="senha123"
        )

        # Cria grupos se não existirem
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        leitor_group, _ = Group.objects.get_or_create(name="Leitor")

        # Adiciona editor ao grupo Editor
        self.editor_user.groups.add(editor_group)

        # Adiciona leitor ao grupo Leitor
        self.reader_user.groups.add(leitor_group)

        # Cria categoria
        self.category, _ = Category.objects.get_or_create(name="Poder", slug="poder")

    def authenticate_as_editor(self):
        self.client.login(username="editor", password="editor123")

    # Teste para criar uma notícia
    def test_create_news(self):
        # Gera o token JWT e Autentica como editor
        response = self.client.post(
            "/api/token/",
            {"username": "editor_test", "password": "senha123"},
            format="json",
        )

        token = response.data["access"]

        # Agora autentica o client com o token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        url = "/api/news/"
        data = {
            "title": "Notícia de Teste Automatizado",
            "subtitle": "Subtítulo da notícia de teste automatizado",
            "content": "Conteúdo da notícia de teste automatizado.",
            "author_id": self.editor_user.id,
            "category_id": self.category.id,
            "status": "draft",
            "pro_only": False,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(News.objects.count(), 1)
        self.assertEqual(News.objects.get().title, "Notícia de Teste Automatizado")

    # Teste para publicar uma notícia
    def test_publish_news(self):
        # Gera o token JWT
        response = self.client.post(
            "/api/token/",
            {"username": "editor_test", "password": "senha123"},
            format="json",
        )

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Cria uma notícia em modo rascunho
        news = News.objects.create(
            title="Notícia Rascunho",
            subtitle="Subtítulo da notícia",
            content="Conteúdo da notícia.",
            author=self.editor_user,
            category=self.category,
            status="draft",
        )

        # Publicar a notícia usando o endpoint de publicação
        url = f"/api/news/{news.id}/publish/"
        response = self.client.post(url, format="json")

        self.assertEqual(response.status_code, 200)
        news.refresh_from_db()
        self.assertEqual(news.status, "published")
        self.assertIsNotNone(news.pub_date)

    # Teste leitor não pode criar uma notícia
    def test_reader_cannot_create_news(self):
        response = self.client.post(
            "/api/token/",
            {"username": "leitor_test", "password": "senha123"},
            format="json",
        )

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Tenta criar uma notícia
        url = "/api/news/"
        data = {
            "title": "Notícia Indevida",
            "subtitle": "Subtítulo",
            "content": "Conteúdo.",
            "author_id": self.reader_user.id,
            "category_id": self.category.id,
            "status": "draft",
            "pro_only": False,
        }
        response = self.client.post(url, data, format="json")

        # Verifica que foi proibido
        self.assertEqual(response.status_code, 403)

    # Teste para garantir que um leitor só vê notícias abertas
    def test_reader_sees_only_open_news(self):
        # Gera o token JWT e autentica como leitor
        response = self.client.post(
            "/api/token/",
            {"username": "leitor_test", "password": "senha123"},
            format="json",
        )

        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Cria uma notícia aberta (pro_only=False)
        News.objects.create(
            title="Notícia Aberta",
            subtitle="Subtítulo aberto",
            content="Conteúdo aberto.",
            author=self.editor_user,
            category=self.category,
            status="published",
            pro_only=False,
        )

        # Cria uma notícia exclusiva PRO (pro_only=True)
        News.objects.create(
            title="Notícia Exclusiva",
            subtitle="Subtítulo exclusivo",
            content="Conteúdo exclusivo.",
            author=self.editor_user,
            category=self.category,
            status="published",
            pro_only=True,
        )

        # Faz a listagem de notícias
        response = self.client.get("/api/news/")

        # Extrai os títulos retornados
        titles = [news["title"] for news in response.data]

        # Validações:
        # - Leitor deve ver a notícia aberta
        self.assertIn("Notícia Aberta", titles)
        # - Leitor não deve ver a notícia exclusiva PRO
        self.assertNotIn("Notícia Exclusiva", titles)

    # Criação de notícia agendada
    def test_create_scheduled_news(self):
        """Verifica se uma notícia agendada é criada com status 'draft' e data futura correta"""
        self.authenticate_as_editor()  # usa helper já existente

        future_time = timezone.now() + timedelta(minutes=5)
        data = {
            "title": "Notícia Agendada",
            "subtitle": "Sub",
            "content": "Conteúdo agendado",
            "author_id": self.editor_user.id,
            "category_id": self.category.id,
            "status": "draft",
            "scheduled_pub_date": future_time.isoformat(),
            "pro_only": False,
        }

        response = self.client.post("/api/news/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(News.objects.count(), 1)
        news = News.objects.first()
        self.assertEqual(news.status, "draft")
        self.assertEqual(
            news.scheduled_pub_date.replace(microsecond=0),
            future_time.replace(microsecond=0),
        )

    # Execução da task Celery que publica a notícia
    def test_publish_scheduled_news_task(self):
        """Verifica se a task 'publish_scheduled_news' publica corretamente uma notícia agendada"""
        past_time = timezone.now() - timedelta(minutes=1)

        News.objects.create(
            title="Agendada para o passado",
            subtitle="Sub",
            content="Conteúdo...",
            author=self.editor_user,
            category=self.category,
            status="draft",
            scheduled_pub_date=past_time,
        )

        # Em vez de esperar o Celery rodar sozinho, chama a task diretamente como uma função
        publish_scheduled_news()

        news = News.objects.first()
        self.assertEqual(news.status, "published")
        self.assertIsNotNone(news.pub_date)

    # Leitor PRO acessa notícia PRO da vertical permitida
    def test_pro_reader_can_access_pro_news_in_allowed_vertical(self):
        # Cria a notícia marcada como PRO
        news = News.objects.create(
            title="Notícia PRO",
            subtitle="Subtítulo PRO",
            content="Conteúdo exclusivo PRO.",
            author=self.editor_user,
            category=self.category,  # categoria "Poder"
            status="published",
            pro_only=True,
        )

        # Gera token para o leitor
        response = self.client.post(
            "/api/token/",
            {"username": "leitor_test", "password": "senha123"},
            format="json",
        )
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # Cria a assinatura do tipo PRO com acesso à categoria da notícia
        Subscription.objects.create(
            user=self.reader_user,
            plan_type="PRO",
        ).verticals.add(self.category)

        # Requisição à API de listagem de notícias
        response = self.client.get("/api/news/")
        self.assertEqual(response.status_code, 200)

        # Deve conter a notícia PRO no resultado
        titles = [item["title"] for item in response.data]
        self.assertIn("Notícia PRO", titles)
