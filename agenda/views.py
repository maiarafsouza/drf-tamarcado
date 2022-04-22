from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer

# Create your views here.

@api_view(http_method_names=['GET'])
def agendamento_detail(request, id):
    obj = get_object_or_404(Agendamento, id=id)
    serializer = AgendamentoSerializer(obj)
    return JsonResponse(serializer.data) # Transforms python dict (serializer.data) in json type response

@api_view(http_method_names=['GET', 'POST'])
def agendamento_list(request):
    if request.method == 'GET':
        qs = Agendamento.objects.all() # qs == queryset
        serializer = AgendamentoSerializer(qs, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        data = request.data # JSON dict
        serializer = AgendamentoSerializer(data=data)
        if serializer.is_valid(): # Validates inputed data and populates validated data attribute in serializer obj
            validated_data = serializer.validated_data
            Agendamento.objects.create(
                data_horario = validated_data['data_horario'],
                nome_cliente = validated_data['nome_cliente'],
                email_cliente = validated_data['email_cliente'],
                telefone_cliente = validated_data['telefone_cliente']
            )
            return JsonResponse(serializer.data, status=201) # 201, standard message for object creation
        return JsonResponse(serializer.errors, status=400)