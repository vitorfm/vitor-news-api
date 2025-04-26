from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from news.models import Category, News


class NewsTests(APITestCase):
    def setUp(self):
        # Cria usuários
        self.editor_user = User.objects.create_user(username='editor_test', password='senha123')
        self.reader_user = User.objects.create_user(username='leitor_test', password='senha123')

        # Cria grupos se não existirem
        editor_group, _ = Group.objects.get_or_create(name='Editor')
        leitor_group, _ = Group.objects.get_or_create(name='Leitor')

        # Adiciona editor ao grupo Editor
        self.editor_user.groups.add(editor_group)

        # Adiciona leitor ao grupo Leitor
        self.reader_user.groups.add(leitor_group)

        # Cria categoria
        self.category, _ = Category.objects.get_or_create(name='Poder', slug='poder')

    # Teste para criar uma notícia
    def test_create_news(self):
        # Gera o token JWT e Autentica como editor
        response = self.client.post('/api/token/', {
            'username': 'editor_test',
            'password': 'senha123'
        }, format='json')

        token = response.data['access']

        # Agora autentica o client com o token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    
        url = '/api/news/'
        data = {
            "title": "Notícia de Teste Automatizado",
            "subtitle": "Subtítulo da notícia de teste automatizado",
            "content": "Conteúdo da notícia de teste automatizado.",
            "author_id": self.editor_user.id,
            "category_id": self.category.id,
            "status": "draft",
            "pro_only": False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(News.objects.count(), 1)
        self.assertEqual(News.objects.get().title, "Notícia de Teste Automatizado")

# Teste para publicar uma notícia
    def test_publish_news(self):
        # Gera o token JWT
        response = self.client.post('/api/token/', {
            'username': 'editor_test',
            'password': 'senha123'
        }, format='json')

        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Cria uma notícia em modo rascunho
        news = News.objects.create(
            title="Notícia Rascunho",
            subtitle="Subtítulo da notícia",
            content="Conteúdo da notícia.",
            author=self.editor_user,
            category=self.category,
            status="draft"
        )

        # Publicar a notícia usando o endpoint de publicação
        url = f'/api/news/{news.id}/publish/'
        response = self.client.post(url, format='json')

        self.assertEqual(response.status_code, 200)
        news.refresh_from_db()
        self.assertEqual(news.status, 'published')
        self.assertIsNotNone(news.pub_date)

    def test_reader_cannot_create_news(self):
        response = self.client.post('/api/token/', {
            'username': 'leitor_test',
            'password': 'senha123'
        }, format='json')

        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Tenta criar uma notícia
        url = '/api/news/'
        data = {
            "title": "Notícia Indevida",
            "subtitle": "Subtítulo",
            "content": "Conteúdo.",
            "author_id": self.reader_user.id,
            "category_id": self.category.id,
            "status": "draft",
            "pro_only": False
        }
        response = self.client.post(url, data, format='json')

        # Verifica que foi proibido
        self.assertEqual(response.status_code, 403)

    # Teste para garantir que um leitor só vê notícias abertas
    def test_reader_sees_only_open_news(self):
        # Gera o token JWT e autentica como leitor
        response = self.client.post('/api/token/', {
            'username': 'leitor_test',
            'password': 'senha123'
        }, format='json')

        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        # Cria uma notícia aberta (pro_only=False)
        News.objects.create(
            title="Notícia Aberta",
            subtitle="Subtítulo aberto",
            content="Conteúdo aberto.",
            author=self.editor_user,
            category=self.category,
            status="published",
            pro_only=False
        )

        # Cria uma notícia exclusiva PRO (pro_only=True)
        News.objects.create(
            title="Notícia Exclusiva",
            subtitle="Subtítulo exclusivo",
            content="Conteúdo exclusivo.",
            author=self.editor_user,
            category=self.category,
            status="published",
            pro_only=True
        )

        # Faz a listagem de notícias
        response = self.client.get('/api/news/')

        # Extrai os títulos retornados
        titles = [news["title"] for news in response.data]

        # Validações:
        # - Leitor deve ver a notícia aberta
        self.assertIn("Notícia Aberta", titles)
        # - Leitor não deve ver a notícia exclusiva PRO
        self.assertNotIn("Notícia Exclusiva", titles)


