from datetime import date
import imp
import requests
from django.conf import settings

def is_feriado(data: date):
    if settings.TESTING == True:
        if data.day == 10 and data.month == 10:
            return True
        return False

    ano = data.year
    r = requests.get(f'https://brasilapi.com.br/api/feriados/v1/{ano}')
    if r.status_code != 200:
        raise ValueError('Não foi possível consultar')
    feriados = r.json()
    for feriado in feriados:
        data_feriado_str = feriado['date']
        data_feriado = date.fromisoformat(data_feriado_str)
        if data_feriado == data:
            return True
    return False