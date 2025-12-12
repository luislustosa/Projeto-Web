from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.index, name='index'),

    # Autenticação e cadastro
    path('cadastro/', views.cadastro_usuario, name='cadastro_usuario'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', views.CustomLogoutView.as_view(), name='logout'),

    # Eventos
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('evento/<int:evento_id>/', views.detalhe_evento, name='detalhe_evento'),
    path('evento/cadastro/', views.cadastro_evento, name='cadastro_evento'),
    path('evento/inscrever/<int:evento_id>/', views.inscrever_evento, name='inscrever_evento'),
    path('meus-eventos/', views.meus_eventos, name='meus_eventos'),



    # Inscrições
    path('minhas_inscricoes/', views.minhas_inscricoes, name='minhas_inscricoes'),

    # Certificados (somente simulação)
    path('certificado/<int:inscricao_id>/', views.certificado_view, name='certificado'),
    path('sobre/', views.sobre, name='sobre'),

    path('evento/<int:evento_id>/deletar/', views.deletar_evento, name='deletar_evento'),
    
    path('api/', include('api.urls')),      
    ]   
