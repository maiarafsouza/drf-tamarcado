from rest_framework import serializers
from agenda.models import Agendamento

class AgendamentoSerializer(serializers.Serializer):
    data_horario = serializers.DateTimeField()
    nome_cliente = serializers.CharField(max_length=200)
    email_cliente = serializers.EmailField()
    telefone_cliente = serializers.CharField(max_length=20)

    # When only validated_data is passed from view to function, the create function is used
    # When instance and validated_data are passed from view to function, the update function is used
    
    def create(self, validated_data):
        agendamento = Agendamento.instance.create(
                data_horario = validated_data['data_horario'],
                nome_cliente = validated_data['nome_cliente'],
                email_cliente = validated_data['email_cliente'],
                telefone_cliente = validated_data['telefone_cliente']
            ) # Creates Agendamento instance from view
        return agendamento
    
    def update(self, instance, validated_data):
        #If data_horario isn't found in dict, the previous value of instance.data_horario (standard value argument) is persisted in memory
        instance.data_horario = validated_data.get('data_horario', instance.data_horario)
        instance.nome_cliente = validated_data.get('nome_cliente', instance.nome_cliente)
        instance.email_cliente = validated_data.get('email_cliente', instance.email_cliente)
        instance.telefone_cliente = validated_data.get('telefone_cliente', instance.telefone_cliente)
        instance.save()
        return instance