from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('dev/', admin.site.urls),
    path('', include('AOHI_users.urls', namespace='users')),
    path('auth/', include('AOHI_auth.urls', namespace='auth')),
    path('admin/', include('AOHI_admin.urls', namespace='aohi_admin')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)