from datetime import datetime, timezone
import json
from urllib import request, response
from rest_framework.test import APITestCase
from agenda.models import Agendamento

# Create your tests here.
# json.dumps(): recieve python data structure (dict) and transforms into json dict
# json.loads(): receive json format (incliding binary) and transforms into python data structure

class TestListaAgendamentos(APITestCase):
    def test_listagem_vazia(self):
        response = self.client.get('/api/agendamentos/') # binary format
        data = json.loads(response.content)
        self.assertEqual(data, [])

    def test_listagem_agendamentos_criados(self):
        Agendamento.objects.create(
            data_horario=datetime(2023, 3, 15, tzinfo=timezone.utc),
            nome_cliente='Alice',
            email_cliente='alice@gmail.com',
            telefone_cliente='99998888',
        )
        
        agendamento_serializado = {
            'id': 1,
            'data_horario': '2023-03-15T00:00:00Z',
            'nome_cliente': 'Alice',
            'email_cliente': 'alice@gmail.com',
            'telefone_cliente': '99998888',
        }

        response = self.client.get('/api/agendamentos/')
        data = json.loads(response.content)
        self.assertDictEqual(data[0], agendamento_serializado)

class TestCriaAgendamento(APITestCase):
    def test_cria_agendamento(self):
        agendamento_request_data = {
            'data_horario': '2023-03-16T00:00:00Z',
            'nome_cliente': 'Alice',
            'email_cliente': 'alice@gmail.com',
            'telefone_cliente': '99998888',
        }
        request = self.client.post('/api/agendamentos/', agendamento_request_data, format='json')
        response = self.client.get('/api/agendamentos/')
        response_data = json.loads(response.content)

        self.assertEqual(response_data[0]['data_horario'], '2023-03-16T00:00:00Z')
        self.assertEqual(response_data[0]['nome_cliente'], 'Alice')
        self.assertEqual(response_data[0]['email_cliente'], 'alice@gmail.com')
        self.assertEqual(response_data[0]['telefone_cliente'], '99998888')
    
    def test_request_inválido_retorna_400(self):
        agendamento_request_data = {
            'data_horario': '2023-03-17T00:00:00Z',
            'nome_cliente': 'Alice',
            'email_cliente': 'alice@gmail.com.br',
            'telefone_cliente': '+1999abc98888',
        }
        response = self.client.post('/api/agendamentos/', agendamento_request_data, format='json')
        self.assertEqual(response.status_code, 400)
    
    def test_agendamentos_mesma_data(self):
        agendamento1_request_data = {
            'data_horario': '2023-03-18T12:00:00Z',
            'nome_cliente': 'Alice',
            'email_cliente': 'alice@gmail.com.br',
            'telefone_cliente': '+1999abc98888',
        }
        agendamento2_request_data = {
            'data_horario': '2023-03-18T13:00:00Z',
            'nome_cliente': 'Alice',
            'email_cliente': 'alice@gmail.com.br',
            'telefone_cliente': '+1999abc98888',
        }
        response1 = self.client.post('/api/agendamentos/', agendamento1_request_data, format='json')
        response2 = self.client.post('/api/agendamentos/', agendamento2_request_data, format='json')
        self.assertEqual(response2.status_code, 400)

