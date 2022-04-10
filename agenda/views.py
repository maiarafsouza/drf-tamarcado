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

@api_view(http_method_names=['GET'])
def agendamento_list(request):
    qs = Agendamento.objects.all() # qs == queryset
    serializer = AgendamentoSerializer(qs, many=True)
    return JsonResponse(serializer.data, safe=False)