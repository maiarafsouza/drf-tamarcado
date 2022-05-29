from datetime import datetime, timezone
import json
from urllib import request
from rest_framework.test import APITestCase
from agenda.models import Agendamento
from django.contrib.auth.models import User

# Create your tests here.
# json.dumps(): recieve python data structure (dict) and transforms into json dict
# json.loads(): receive json format (incliding binary) and transforms into python data structure

class TestListaAgendamentos(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username="bob", password="123")
        other_user = User.objects.create_user(username="carolina", password="456")

    def test_listagem_vazia(self):
        user = User.objects.get(username='bob')
        self.client.force_authenticate(user)
        response = self.client.get('/api/agendamentos/?username=bob') # binary format response
        data = json.loads(response.content)
        self.assertEqual(data, [])

    def test_listagem_agendamentos_criados(self):

        Agendamento.objects.create(
            data_horario=datetime(2023, 3, 15, tzinfo=timezone.utc),
            prestador=User.objects.get(username='bob'),
            nome_cliente='Alice',
            email_cliente='alice@gmail.com',
            telefone_cliente='99998888'
        )
        
        agendamento_serializado = {
            'id': 1,
            'data_horario': '2023-03-15T00:00:00Z',
            'prestador': 'bob',
            'nome_cliente': 'Alice',
            'email_cliente': 'alice@gmail.com',
            'telefone_cliente': '99998888'
        }

        self.client.login(username="bob", password="123")
        response = self.client.get('/api/agendamentos/?username=bob')
        data = json.loads(response.content)
        self.assertDictEqual(data[0], agendamento_serializado)

    def test_listagem_outro_usuario(self):
        other_user = User.objects.get(username='carolina')
        self.client.force_authenticate(other_user)
        response = self.client.get('/api/agendamentos/?username=bob') # binary format response
        self.assertEqual(response.status_code, 403)

class TestCriaAgendamento(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username="bob", password="123")

    def test_cria_agendamento(self):
        agendamento_request_data = {
            'data_horario': '2023-03-16T12:00:00Z',
            'prestador': 'bob',
            'nome_cliente': 'Alice',
            'email_cliente': 'alice@gmail.com',
            'telefone_cliente': '99998888'
        }
        request = self.client.post('/api/agendamentos/', agendamento_request_data, format='json')
        self.client.login(username="bob", password="123")
        response = self.client.get('/api/agendamentos/?username=bob')
        response_data = json.loads(response.content)

        self.assertEqual(response_data[0]['data_horario'], '2023-03-16T12:00:00Z')
        self.assertEqual(response_data[0]['prestador'], 'bob')
        self.assertEqual(response_data[0]['nome_cliente'], 'Alice')
        self.assertEqual(response_data[0]['email_cliente'], 'alice@gmail.com')
        self.assertEqual(response_data[0]['telefone_cliente'], '99998888')
    
    def test_request_inválido_retorna_400(self):
        agendamento_request_data = {
            'data_horario': '2023-03-17T00:00:00Z',
            'nome_cliente': 'Alice',
            'email_cliente': 'alice@gmail.com.br',
            'telefone_cliente': '+1999abc98888'
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

class TestDetalhaAgendamento(APITestCase):
    def setUp(self):
        user = User.objects.create_user(username="bob", password="123")
        agendamento = Agendamento.objects.create(data_horario='2023-03-16T09:00:00Z', prestador=User.objects.get(username='bob'), nome_cliente='Alice', email_cliente='alice@gmail.com', telefone_cliente='99998888')

    def test_detalha_agendamento(self):
        self.client.login(username="bob", password="123")
        response = self.client.get('/api/agendamentos/1')
        response_data = json.loads(response.content)

        self.assertEqual(response_data['data_horario'], '2023-03-16T09:00:00Z')
        self.assertEqual(response_data['prestador'], 'bob')
        self.assertEqual(response_data['nome_cliente'], 'Alice')
        self.assertEqual(response_data['email_cliente'], 'alice@gmail.com')
        self.assertEqual(response_data['telefone_cliente'], '99998888')

class TestGetHorarios(APITestCase):
    def test_quando_feriado_retorna_lista_vazia(self):
        response = self.client.get('/api/horarios/?data=2022-10-10')
        py_response = json.loads(response.content)
        self.assertEqual(py_response, [])
        
    def test_quando_dia_util_retorna_horarios(self):
        response = self.client.get('/api/horarios/?data=2022-10-03')
        py_response = json.loads(response.content)
        self.assertNotEqual(py_response, [])
        self.assertEqual(py_response[0], '2022-10-03T09:00:00Z')
        self.assertEqual(py_response[-1], '2022-10-03T17:30:00Z')