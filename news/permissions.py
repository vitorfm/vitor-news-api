from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Permite acesso apenas para usuários administradores.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
        Permite que apenas o autor edite/exclua OU admins editem qualquer coisa.
    """
    def has_object_permission(self, request, view, obj):
        # Permissões de leitura são permitidas para qualquer solicitação
        if request.method in permissions.SAFE_METHODS:
            return True

        # Admins têm permissão total
        if request.user.is_staff:
            return True

        # Edição apenas para o autor
        return obj.author == request.user


class IsEditorOrAdminPermission(permissions.BasePermission):
    """
    Permite acesso apenas para Admins ou usuários do grupo Editor.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.is_staff:
            return True  # Admin tem acesso total

        return user.groups.filter(name='Editor').exists()
    
class HasAccessToContent(permissions.BasePermission):
    """
    Verifica se o usuário tem acesso ao conteúdo com base em sua assinatura.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        
        # Admins têm acesso a tudo
        if user.is_staff:
            return True
            
        # Se o conteúdo não é PRO, qualquer um pode acessar
        if not obj.pro_only:
            return True
            
        # Verificar se o usuário tem assinatura
        try:
            subscription = user.subscription
        except:
            return False

        if not subscription.is_pro:
            # Usuário não é PRO → não pode acessar conteúdo exclusivo
            return False
            
        # Se for PRO, verificar se tem acesso à vertical da notícia
        category_name = obj.category.name.lower()

       
        if category_name in ['poder'] and subscription.has_poder:
            return True
        elif category_name in ['tributos'] and subscription.has_tributos:
            return True
        elif category_name in ['saude', 'saúde'] and subscription.has_saude:
            return True
        elif category_name in ['energia'] and subscription.has_energia:
            return True
        elif category_name in ['trabalhista'] and subscription.has_trabalhista:
            return True

        return False