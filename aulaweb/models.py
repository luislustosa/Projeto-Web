from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta


class Usuario(AbstractUser):
    PERFIL_CHOICES = (
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
        ('organizador', 'Organizador'),
    )
    telefone = models.CharField("Telefone", max_length=20, blank=True)
    instituicao = models.CharField("Instituição", max_length=150, blank=True)
    perfil = models.CharField("Perfil", max_length=20, choices=PERFIL_CHOICES, default='aluno')

    # Evita conflito com auth.User.groups / user_permissions
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',
        blank=True,
        help_text='Grupos deste usuário.'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permissions_set',
        blank=True,
        help_text='Permissões específicas do usuário.'
    )

    def __str__(self):
        return self.get_full_name() or self.username


class Evento(models.Model):
    TIPO_EVENTO = (
        ('seminario', 'Seminário'),
        ('palestra', 'Palestra'),
        ('workshop', 'Workshop'),
        ('minicurso', 'Minicurso'),
        ('semana', 'Semana Acadêmica')
    )

    nome = models.CharField("Nome do evento", max_length=200)
    tipo = models.CharField("Tipo", max_length=20, choices=TIPO_EVENTO)

    data_inicio = models.DateField("Data inicial")
    data_fim = models.DateField("Data final")

    hora_inicio = models.TimeField("Hora inicial", default='08:00:00')
    hora_fim = models.TimeField("Hora final", null=True, blank=True)

    local = models.CharField("Local", max_length=200)
    max_participantes = models.PositiveIntegerField("Limite de participantes", default=0)

    organizador = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        limit_choices_to={'perfil': 'organizador'}
    )

    horario = models.TimeField()

    banner = models.ImageField(
        upload_to='banners/',  # pasta dentro de MEDIA_ROOT
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class Inscricao(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    data_inscricao = models.DateTimeField(auto_now_add=True)
    certificado_emitido = models.BooleanField(default=False)

    class Meta:
        unique_together = ('usuario', 'evento')
        ordering = ['-data_inscricao']

    def __str__(self):
        return f"{self.usuario} -> {self.evento}"


# Opcional: manter histórico de certificados gerados
class Certificado(models.Model):
    inscricao = models.OneToOneField(Inscricao, on_delete=models.CASCADE)
    emitido_em = models.DateTimeField(auto_now_add=True)
    arquivo = models.FileField(upload_to='certificados/', blank=True, null=True)

    def __str__(self):
        return f"Certificado: {self.inscricao}"

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Evento, Inscricao

@login_required
def meus_eventos(request):
    # Filtra eventos criados pelo usuário logado
    eventos = Evento.objects.filter(organizador=request.user)
    
    # Para cada evento, contamos quantas pessoas estão inscritas
    eventos_info = []
    for evento in eventos:
        inscritos = Inscricao.objects.filter(evento=evento).count()
        eventos_info.append({
            'evento': evento,
            'inscritos': inscritos
        })
    
    return render(request, 'aulaweb/meus_eventos.html', {
        'eventos_info': eventos_info
    })





class ConfirmacaoCadastro(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    expiracao = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(64)
        if not self.expiracao:
            self.expiracao = timezone.now() + timedelta(days=1)  # 24h de validade
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Confirmação para {self.usuario.username}"

