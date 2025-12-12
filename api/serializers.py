from rest_framework import serializers
from aulaweb.models import Usuario, Evento, Inscricao

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'telefone', 'instituicao', 'perfil']

class EventoSerializer(serializers.ModelSerializer):
    organizador = UsuarioSerializer(read_only=True)

    class Meta:
        model = Evento
        fields = ['id', 'nome', 'tipo', 'data_inicio', 'data_fim', 'horario', 'local', 'max_participantes', 'organizador']

class InscricaoSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    evento = EventoSerializer(read_only=True)

    class Meta:
        model = Inscricao
        fields = ['id', 'usuario', 'evento', 'data_inscricao', 'certificado_emitido']

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'