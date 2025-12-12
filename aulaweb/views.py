# aulaweb/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm

from .models import Usuario, Evento, Inscricao
from .forms import UsuarioCreationForm, LoginForm, EventoForm

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UsuarioCreationForm
from .models import ConfirmacaoCadastro, Usuario

from django.utils import timezone
from django.shortcuts import get_object_or_404

# ========== AUTENTICAÇÃO ==========
def cadastro_usuario(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_active = False  # bloqueia login até confirmar
            usuario.save()
            
            # Cria token de confirmação
            confirmacao = ConfirmacaoCadastro.objects.create(usuario=usuario)
            
            # Monta link de ativação
            link = request.build_absolute_uri(
                reverse('ativar_usuario', kwargs={'token': confirmacao.token})
            )
            
            # Envio do e-mail
            assunto = "Bem-vindo ao SGEA!"
            mensagem = f"""
            Olá {usuario.username}!

            Bem-vindo ao sistema SGEA.

            Clique no link abaixo para ativar sua conta:
            {link}

            Atenciosamente,
            Equipe SGEA
            """
            send_mail(
                assunto,
                mensagem,
                None,
                [usuario.email],
                fail_silently=False,
            )

            return render(request, 'aulaweb/aguardando_confirmacao.html')
    else:
        form = UsuarioCreationForm()
    return render(request, 'aulaweb/cadastro_usuario.html', {'form': form})


def login_usuario(request):
    """Realiza login do usuário com mensagens de sucesso ou erro."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, f"Bem-vindo, {username}!")
                return redirect('index')
            elif user is not None and not user.is_active:
                messages.error(request, "Usuário inativo.")
            else:
                messages.error(request, "Usuário ou senha inválidos.")
        else:
            messages.error(request, "Erro ao autenticar. Verifique o username e a senha.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'aulaweb/login.html', {'form': form})

def logout_usuario(request):
    """Efetua logout do usuário e exibe mensagem."""
    logout(request)
    messages.info(request, "Você saiu da sua conta.")
    return redirect('login_usuario')


class CustomLoginView(LoginView):
    """Tela de login personalizada."""
    template_name = 'aulaweb/login.html'
    authentication_form = LoginForm


class CustomLogoutView(LogoutView):
    """Logout com redirecionamento automático para a página inicial."""
    next_page = '/'



def ativar_usuario(request, token):
    confirmacao = get_object_or_404(ConfirmacaoCadastro, token=token)
    if confirmacao.expiracao < timezone.now():
        return render(request, 'aulaweb/token_expirado.html')
    
    usuario = confirmacao.usuario
    usuario.is_active = True
    usuario.save()
    
    confirmacao.delete()  # token usado, remove do banco
    
    return render(request, 'aulaweb/usuario_ativado.html', {'usuario': usuario})


# ========== PÁGINAS PRINCIPAIS ==========

def index(request):
    """
    Página inicial do site.
    Mostra todos os eventos existentes, ranqueados pelo número de inscrições.
    """
    eventos = Evento.objects.all()

    eventos_info = []
    for evento in eventos:
        inscritos = Inscricao.objects.filter(evento=evento).count()
        eventos_info.append({'evento': evento, 'inscritos': inscritos})

    eventos_info.sort(key=lambda x: x['inscritos'], reverse=True)

    return render(request, 'aulaweb/index.html', {'eventos_info': eventos_info})


def sobre(request):
    """Página 'Sobre' institucional."""
    return render(request, 'aulaweb/sobre.html')


# ========== EVENTOS ==========

@login_required
def lista_eventos(request):
    """Lista todos os eventos disponíveis."""
    eventos = Evento.objects.all().order_by('data_inicio')
    return render(request, 'aulaweb/lista_eventos.html', {'eventos': eventos})


@login_required
def detalhe_evento(request, evento_id):
    """Exibe os detalhes de um evento específico."""
    evento = get_object_or_404(Evento, id=evento_id)
    ja_inscrito = Inscricao.objects.filter(usuario=request.user, evento=evento).exists()
    return render(request, 'aulaweb/detalhe_evento.html', {'evento': evento, 'ja_inscrito': ja_inscrito})


@login_required
def cadastro_evento(request):
    """Permite que um organizador cadastre um novo evento."""
    if request.user.perfil != 'organizador':
        messages.error(request, "Apenas organizadores podem cadastrar eventos.")
        return redirect('lista_eventos')

    if request.method == 'POST':
        # Passa também request.FILES para lidar com upload de imagens
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.organizador = request.user  # define automaticamente o organizador
            evento.save()
            messages.success(request, "Evento cadastrado com sucesso!")
            return redirect('lista_eventos')
        else:
            messages.error(request, "Corrija os erros no formulário.")
    else:
        form = EventoForm()

    return render(request, 'aulaweb/cadastro_evento.html', {'form': form})


@login_required
def deletar_evento(request, evento_id):
    """Permite que o organizador exclua um evento."""
    evento = get_object_or_404(Evento, id=evento_id)

    if evento.organizador != request.user:
        messages.error(request, "Você não tem permissão para excluir este evento.")
        return redirect('detalhe_evento', evento_id=evento.id)

    if request.method == "POST":
        evento.delete()
        messages.success(request, "Evento excluído com sucesso!")
        return redirect('lista_eventos')

    return render(request, 'aulaweb/confirmar_exclusao.html', {'evento': evento})


@login_required
def meus_eventos(request):
    """
    Exibe os eventos criados pelo usuário logado.
    Mostra detalhes de cada evento e quantidade de inscritos.
    """
    eventos = Evento.objects.filter(organizador=request.user)
    eventos_info = []

    for evento in eventos:
        inscritos = Inscricao.objects.filter(evento=evento).count()
        eventos_info.append({'evento': evento, 'inscritos': inscritos})

    return render(request, 'aulaweb/meus_eventos.html', {'eventos_info': eventos_info})


# ========== INSCRIÇÕES ==========

@login_required
def inscrever_evento(request, evento_id):
    """Realiza a inscrição do usuário em um evento."""
    evento = get_object_or_404(Evento, id=evento_id)
    total = Inscricao.objects.filter(evento=evento).count()

    if evento.max_participantes and total >= evento.max_participantes:
        messages.error(request, "Evento cheio. Não é possível se inscrever.")
        return redirect('detalhe_evento', evento_id=evento.id)

    inscricao, created = Inscricao.objects.get_or_create(usuario=request.user, evento=evento)
    if created:
        messages.success(request, f"Inscrição realizada em {evento.nome}!")
    else:
        messages.info(request, "Você já está inscrito neste evento.")

    return redirect('minhas_inscricoes')


@login_required
def minhas_inscricoes(request):
    """Lista todas as inscrições do usuário logado."""
    inscricoes = Inscricao.objects.filter(usuario=request.user).select_related('evento')
    return render(request, 'aulaweb/minhas_inscricoes.html', {'inscricoes': inscricoes})


# ========== CERTIFICADOS ==========

@login_required
def certificado_view(request, inscricao_id):
    """Exibe (ou simula) a emissão de certificado."""
    inscricao = get_object_or_404(Inscricao, id=inscricao_id)

    if inscricao.usuario != request.user and inscricao.evento.organizador != request.user:
        messages.error(request, "Você não tem permissão para visualizar este certificado.")
        return redirect('index')

    if not inscricao.certificado_emitido:
        inscricao.certificado_emitido = True
        inscricao.save()
        messages.success(request, "Certificado emitido com sucesso (simulação).")

    return render(request, 'aulaweb/certificado_preview.html', {'inscricao': inscricao})


# ========== API ==========

from django.http import JsonResponse

def api(request):
    """Endpoint simples de teste da API."""
    return JsonResponse({"mensagem": "API funcionando!"})
