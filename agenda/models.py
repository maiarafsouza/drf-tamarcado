import email
from django.db import models

# Create your models here.

class Agendamento(models.Model):
    data_horario = models.DateTimeField()
    nome_cliente = models.CharField(max_length=200)
    email_cliente = models.EmailField()
    telefone_cliente = models.CharField(max_length=20)
    status_cancelado = models.BooleanField(default=False) # Creates attribute canceled, set default at obj creation as False
