from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NewsViewSet, CategoryViewSet, UserViewSet, SubscriptionViewSet

# Criar router e registrar nossos viewsets
router = DefaultRouter()
router.register(r"news", NewsViewSet)
router.register(r"categories", CategoryViewSet)
router.register(r"users", UserViewSet)
router.register(r"subscriptions", SubscriptionViewSet)

# URLs da API
urlpatterns = [
    path("", include(router.urls)),
]
