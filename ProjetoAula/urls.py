from django.contrib import admin
from django.urls import path, include
from django.conf import settings           # ⚡ importar settings
from django.conf.urls.static import static # ⚡ importar static
from django.urls import path
from aulaweb import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('aulaweb.urls')),
    path('cadastro/', views.cadastro_usuario, name='cadastro_usuario'),
    path('ativar/<str:token>/', views.ativar_usuario, name='ativar_usuario'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
