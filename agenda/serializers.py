import re
from rest_framework import serializers
from datetime import datetime, date
from django.utils import timezone
from django.contrib.auth.models import User
from agenda.models import Agendamento
from agenda.utils import get_horarios_disponiveis

class AgendamentoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Agendamento
        fields = ['id', 'data_horario', 'nome_cliente', 'email_cliente', 'telefone_cliente', 'prestador']  # datetime: YYYY-MM-DD-Thh:mm

    prestador = serializers.CharField()
    def validate_prestador(self, value):
        try:
            prestador_obj = User.objects.get(username=value)
            return prestador_obj
        except User.DoesNotExist:
            raise serializers.ValidationError('Usuário não existe!')
        return prestador_obj

    def validate_data_horario(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('Agendamento só pode ser feito para futuro!')
        
        if value not in get_horarios_disponiveis(value.date()):
            raise serializers.ValidationError('Esse horário não está disponível!')
        return value
    
    def validate_telefone_cliente(self, attrs):
        telefone_cliente = attrs
        invalid_characters = re.compile(r'[^\d+( )]')
        invalid_telephone = invalid_characters.findall(telefone_cliente)
        
        if len(telefone_cliente) < 8:
            raise serializers.ValidationError('Telefone deve ter pelo menos 8 caracteres')
        
        if invalid_telephone != []:
            raise serializers.ValidationError(f'Caracteres {invalid_telephone} não permitidos')

        if '+' in telefone_cliente and '+' in telefone_cliente[1:]:
                raise serializers.ValidationError('Número inválido')
        
        return attrs
    
    def validate(self, attrs):
        email_cliente = attrs.get('email_cliente', '')
        telefone_cliente = attrs.get('telefone_cliente', '')
        data_horario = attrs.get('data_horario', '')

        if email_cliente.endswith('.br') and telefone_cliente.startswith('+') and not telefone_cliente.startswith('+55'):
            raise serializers.ValidationError('Email brasileiro deve estar associado a telefone brasileiro (+55)')

        if 'data_horario' in attrs:
            data_agendamento = data_horario.date()
            agendamentos_cliente = Agendamento.objects.filter(email_cliente=email_cliente, data_horario__date=data_agendamento, status_cancelado=False)
            if list(agendamentos_cliente.values()) != []:
                raise serializers.ValidationError('Usuário já tem agendamento nesta data')

        return attrs

    # When only validated_data is passed from view to function, the create function is used
    # When instance and validated_data are passed from view to function, the update function is used
    # Model Serializers have create and update methods by default

class PrestadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'agendamentos'] # agendamentos comes from related_name on Agendamentos prestador primary key field
    
    agendamentos = AgendamentoSerializer(many=True, read_only=True)
    
    # def create(self, validated_data):
    #    agendamento = Agendamento.instance.create(
    #            data_horario = validated_data['data_horario'],
    #            nome_cliente = validated_data['nome_cliente'],
    #            email_cliente = validated_data['email_cliente'],
    #            telefone_cliente = validated_data['telefone_cliente']
    #        ) # Creates Agendamento instance from view
    #    return agendamento
    
    # def update(self, instance, validated_data):
        #If data_horario isn't found in dict, the previous value of instance.data_horario (standard value argument) is persisted in memory
    #    instance.data_horario = validated_data.get('data_horario', instance.data_horario)
    #    instance.nome_cliente = validated_data.get('nome_cliente', instance.nome_cliente)
    #    instance.email_cliente = validated_data.get('email_cliente', instance.email_cliente)
    #    instance.telefone_cliente = validated_data.get('telefone_cliente', instance.telefone_cliente)
    #    instance.save()
    #    return instance