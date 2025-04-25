from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth.models import User
from django.utils import timezone
from .models import News, Category, Subscription
from .serializers import NewsSerializer, CategorySerializer, UserSerializer, SubscriptionSerializer
from .permissions import IsAuthorOrReadOnly, HasAccessToContent

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
        else:
            permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Filtra o queryset com base no usuário:
        - Admin: vê tudo
        - Editor: vê tudo (mas só pode editar as próprias)
        - Leitor comum: vê apenas as publicadas
        """
        user = self.request.user
        
        # Se for admin, vê tudo
        if user.is_staff:
            return News.objects.all()
            
        # Se for um editor, vê as próprias e as publicadas
        if News.objects.filter(author=user).exists():
            return News.objects.filter(author=user) | News.objects.filter(status='published')
            
        # Se for leitor comum, vê apenas as publicadas
        return News.objects.filter(status='published')
    
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
        
        serializer = self.get_serializer(news)
        return Response(serializer.data)
    