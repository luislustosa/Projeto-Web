from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario, Evento, Inscricao
import re
# ==============================
# Formulário de criação de usuário
# ==============================



class UsuarioCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    telefone = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(XX) XXXXX-XXXX', 'id': 'id_telefone'})
    )
    instituicao = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Instituição'})
    )

    class Meta:
        model = Usuario
        fields = ("username", "email", "telefone", "instituicao", "perfil", "password1", "password2")
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuário'}),
            'perfil': forms.Select(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirme a senha'}),
        }

    # Validação de telefone
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            pattern = r'^\(\d{2}\) \d{4,5}-\d{4}$'
            if not re.match(pattern, telefone):
                raise forms.ValidationError("Telefone inválido. Formato esperado: (XX) XXXXX-XXXX")
        return telefone

    # Validação de email
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está em uso.")
        return email


# ==============================
# Formulário de login
# ==============================
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Usuário", 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Senha", 
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

# ==============================
# Formulário de Evento
# ==============================
from django import forms
from .models import Evento
from PIL import Image
import re

class EventoForm(forms.ModelForm):
    # Campos do formulário
    nome = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    tipo = forms.ChoiceField(choices=Evento.TIPO_EVENTO, widget=forms.Select(attrs={'class': 'form-control'}))
    data_inicio = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'data_inicio'}))
    data_fim = forms.DateField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'data_fim'}))
    hora_inicio = forms.TimeField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'hora_inicio'}))
    hora_fim = forms.TimeField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'hora_fim'}))
    local = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    max_participantes = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    banner = forms.ImageField(required=False)

    class Meta:
        model = Evento
        fields = [
            'nome', 'tipo', 'data_inicio', 'data_fim', 'hora_inicio',
            'hora_fim', 'local', 'max_participantes', 'organizador', 'banner'
        ]

    # Validação de banner
    def clean_banner(self):
        banner = self.cleaned_data.get('banner')
        if banner:
            # Verifica tipo de arquivo
            if not banner.content_type in ['image/jpeg', 'image/png']:
                raise forms.ValidationError("A imagem deve ser PNG ou JPEG.")
            # Verifica tamanho máximo
            if banner.size > 2*1024*1024:
                raise forms.ValidationError("A imagem não pode ultrapassar 2MB.")
            # Verifica se é realmente uma imagem
            try:
                Image.open(banner).verify()
            except Exception:
                raise forms.ValidationError("Arquivo inválido. Não é uma imagem.")
        return banner

    # Validação de datas
    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fim = cleaned_data.get('hora_fim')

        if data_inicio and data_fim:
            if data_fim < data_inicio:
                raise forms.ValidationError("A data final não pode ser anterior à data inicial.")

        if hora_inicio and hora_fim:
            if hora_fim < hora_inicio:
                raise forms.ValidationError("A hora final não pode ser anterior à hora inicial.")

        return cleaned_data


# ==============================
# Formulário de Inscrição
# ==============================
class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = []  # será criado automaticamente no backend
