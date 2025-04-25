from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Permite acesso apenas para usuários administradores.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permite que editores modifiquem apenas suas próprias notícias.
    """
    def has_object_permission(self, request, view, obj):
        # Permissões de leitura são permitidas para qualquer solicitação
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permissões de escrita apenas para o autor da notícia
        return obj.author == request.user

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
            
        # Verificar se usuário é PRO e tem acesso à vertical específica
        if subscription.is_pro:
            category_name = obj.category.name.lower()
            
            if category_name == 'poder' and subscription.has_poder:
                return True
            elif category_name == 'tributos' and subscription.has_tributos:
                return True
            elif category_name == 'saude' and subscription.has_saude:
                return True
            elif category_name == 'energia' and subscription.has_energia:
                return True
            elif category_name == 'trabalhista' and subscription.has_trabalhista:
                return True
                
        return False