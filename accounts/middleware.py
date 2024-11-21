from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class RolePermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Admin her yere erişebilir
            if request.user.is_superuser:
                return self.get_response(request)

            # Kullanıcının rolü varsa izinlerini kontrol et
            if request.user.role:
                current_path = request.path_info
                permissions = request.user.role.permissions

                # İzin kontrolü
                if not self._has_permission(current_path, permissions):
                    messages.error(request, "You don't have permission to access this page.")
                    return redirect('accounts:dashboard')

        return self.get_response(request)

    def _has_permission(self, path, permissions):
        # İzin kontrolü mantığı
        # permissions JSON'ında sayfa izinleri kontrol edilecek
        allowed_paths = permissions.get('allowed_paths', [])
        return any(path.startswith(allowed_path) for allowed_path in allowed_paths)