from datetime import date
import requests
from django.conf import settings
import os
import logging

def is_feriado(data: date):
    logging.info(f'Fazendo requisição para BrasilAPI para data: {data.isoformat()}')
    if settings.TESTING == True:
        logging.info(f'Requisição para BrasilAPI com TESTING=True')
        if data.day == 10 and data.month == 10:
            return True
        return False

    ano = data.year

    BRASIL_API_URL = os.environ.get('BRASIL_API_URL', 'https://brasilapi.com.br/')
    r = requests.get(f'{BRASIL_API_URL}{ano}')
    if r.status_code != 200:
        logging.error('Erro na requisição para BrasilAPI')
        return False
    feriados = r.json()
    for feriado in feriados:
        data_feriado_str = feriado['date']
        data_feriado = date.fromisoformat(data_feriado_str)
        if data_feriado == data:
            return True
    return False