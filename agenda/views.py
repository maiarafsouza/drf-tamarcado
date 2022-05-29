from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer, PrestadorSerializer
from agenda.utils import get_horarios_disponiveis

# Create your views here.

class IsOwnerOrCreateOnly(permissions.BasePermission): # API/URL level permission
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        username = request.query_params.get('username', None)
        if request.user.username == username:
            return True
        return False

class IsPrestador(permissions.BasePermission): # Object level permission
    def has_object_permission(self, request, view, obj):
        if obj.prestador == request.user:
            return True
        return False

class AgendamentoDetail(RetrieveUpdateDestroyAPIView): # /api/agendamentos/<id>
    serializer_class = AgendamentoSerializer
    lookup_field = 'id'
    queryset = Agendamento.objects.all()
    permission_classes = [IsPrestador]

    def perform_destroy(self, obj):
        obj.status_cancelado = True
        obj.save()

class AgendamentoList(ListCreateAPIView): # /api/agendamentos/?username=name
    serializer_class = AgendamentoSerializer
    permission_classes = [IsOwnerOrCreateOnly]
    def get_queryset(self):
        username = self.request.query_params.get('username', None)
        queryset = Agendamento.objects.filter(prestador__username=username, status_cancelado=False)
        return queryset

class PrestadorList(ListAPIView): # /api/prestadores
    serializer_class = PrestadorSerializer
    queryset = User.objects.all()


@api_view(http_method_names=['GET']) # 
def get_horarios(request):
    data = request.query_params.get('data')
    if not data:
        data = datetime.now().date()
    else:
        data = datetime.fromisoformat(data).date()
    
    horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))
    return JsonResponse(horarios_disponiveis, safe=False)

