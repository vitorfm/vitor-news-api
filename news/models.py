from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    """Categoria (ou vertical) de notícias"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"

class Subscription(models.Model):
    """Assinatura de um usuário, definindo seu plano"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    is_pro = models.BooleanField(default=False)
    
    # Verticais disponíveis para o usuário
    has_poder = models.BooleanField(default=False)
    has_tributos = models.BooleanField(default=False)
    has_saude = models.BooleanField(default=False)
    has_energia = models.BooleanField(default=False)
    has_trabalhista = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {'PRO' if self.is_pro else 'INFO'}"

class News(models.Model):
    """Notícia"""
    STATUS_CHOICES = (
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
    )
    
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    content = models.TextField()
    pub_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='news')
    pro_only = models.BooleanField(default=False, help_text="Define se o conteúdo é exclusivo para usuários PRO")
    scheduled_pub_date = models.DateTimeField(null=True, blank=True, help_text="Data agendada para publicação automática.")

    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = "News"