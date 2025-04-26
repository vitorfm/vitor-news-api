from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.utils import timezone
from .models import News, Category, Subscription
from .serializers import NewsSerializer, CategorySerializer, UserSerializer, SubscriptionSerializer
from .permissions import IsAuthorOrReadOnly, HasAccessToContent, IsEditorOrAdminPermission
from .tasks import send_notification_email
from .tasks import send_real_email

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAdminUser]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_subscription(self, request):
        """Endpoint para buscar a assinatura do usuário logado"""
        try:
            subscription = Subscription.objects.get(user=request.user)
            serializer = self.get_serializer(subscription)
            return Response(serializer.data)
        except Subscription.DoesNotExist:
            return Response(
                {"error": "Nenhuma assinatura encontrada para este usuário"}, 
                status=status.HTTP_404_NOT_FOUND
            )

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'subtitle', 'content']
    
    def get_permissions(self):
        """
        Define permissões com base na ação:
        - Listar/Visualizar: Verificar acesso ao conteúdo
        - Criar/Editar/Deletar: Ser autor ou admin
        """
        if self.action in ['retrieve', 'list']:
            permission_classes = [IsAuthenticated, HasAccessToContent]
        elif self.action in ['create', 'update', 'partial_update', 'destroy', 'publish']:
            permission_classes = [IsAuthenticated, IsEditorOrAdminPermission, IsAuthorOrReadOnly]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filtra o queryset com base no usuário:
        - Admin: vê tudo
        - Editor: vê tudo (mas só pode editar as próprias)
        - Leitor comum: vê apenas as publicadas
    
        Filtra as notícias com base no tipo de usuário e sua assinatura.

        """
        user = self.request.user
        
        # Se for admin, vê tudo
        if user.is_staff:
            return News.objects.all()
            
        # Se for um editor, vê as próprias e as publicadas
        if News.objects.filter(author=user).exists():
            return News.objects.filter(author=user) | News.objects.filter(status='published')
            
         # Leitor comum (INFO ou PRO)
        queryset = News.objects.filter(status='published')

        if not hasattr(user, 'subscription'):
            # Se o usuário não tem assinatura, vê apenas notícias abertas
            return queryset.filter(pro_only=False)
        
        subscription = user.subscription

        if not subscription.is_pro:
            # Se não é PRO, vê apenas notícias abertas
            return queryset.filter(pro_only=False)
        
        # Se for PRO, filtrar de acordo com as verticais contratadas
        ids_permitidos = []
        for news in queryset:
            category_name = news.category.name.lower()

            if category_name in ['poder'] and subscription.has_poder:
                ids_permitidos.append(news.id)
            elif category_name in ['tributos'] and subscription.has_tributos:
                ids_permitidos.append(news.id)
            elif category_name in ['saude', 'saúde'] and subscription.has_saude:
                ids_permitidos.append(news.id)
            elif category_name in ['energia'] and subscription.has_energia:
                ids_permitidos.append(news.id)
            elif category_name in ['trabalhista'] and subscription.has_trabalhista:
                ids_permitidos.append(news.id)

            # Notícias abertas sempre permitidas
            if not news.pro_only:
                ids_permitidos.append(news.id)
        
        return News.objects.filter(id__in=ids_permitidos)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAuthorOrReadOnly])
    def publish(self, request, pk=None):
        """Endpoint para publicar uma notícia"""
        news = self.get_object()
        
        if news.status == 'published':
            return Response(
                {"error": "Esta notícia já está publicada"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        news.status = 'published'
        news.pub_date = timezone.now()
        news.save()

        send_notification_email.delay(news.id, news.title)

        # Exemplo de uso:
        send_real_email.delay('vitor.monteiro@gmail.com', news.title)

        send_real_email.apply_async(
            args=['vitor.fariamonteiro@gmail.com', news.title],
            countdown=60  # segundos
        )
        
        serializer = self.get_serializer(news)
        return Response(serializer.data)
    