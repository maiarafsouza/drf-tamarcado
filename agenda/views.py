from functools import partial
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer

# Create your views here.

@api_view(http_method_names=['GET', 'PUT', 'PATCH', 'DELETE'])
def agendamento_detail(request, id):
    if request.method == 'GET':
        obj = get_object_or_404(Agendamento, id=id)
        serializer = AgendamentoSerializer(obj)
        return JsonResponse(serializer.data) # Transforms python dict (serializer.data) in json type response

    if request.method == 'PATCH': # Subtitutes obj partialy
        obj = get_object_or_404(Agendamento, id=id)
        serializer = AgendamentoSerializer(obj, data=request.data, partial=True) # partial=True, accepts partial data on this serializer instance
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)

#    if request.method == 'PUT': # Subtitutes obj entirely
        obj = get_object_or_404(Agendamento, id=id)
        serializer = AgendamentoSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    
    if request.method == 'DELETE':
        obj = get_object_or_404(Agendamento, id=id)
        obj.status_cancelado = True # Changes canceled attribute
        obj.save()
        return Response(status=204)

@api_view(http_method_names=['GET', 'POST'])
def agendamento_list(request):
    if request.method == 'GET':
        qs = Agendamento.objects.exclude(status_cancelado=True) # qs == queryset, excludes canceled events
        serializer = AgendamentoSerializer(qs, many=True)
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        data = request.data # JSON dict
        serializer = AgendamentoSerializer(data=data)
        if serializer.is_valid(): # Validates inputed data and populates validated data attribute in serializer obj
            validated_data = serializer.validated_data
            serializer.save() # Calls AgendamentoSerializers.create
            return JsonResponse(serializer.data, status=201) # 201, standard message for object creation
        return JsonResponse(serializer.errors, status=400)