from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from game.models import Game, Turn
from game.serializers import GameSerializer


# Create your tests here.
class GameAPITest(APITestCase):
    def test_game(self):
        user = User.objects.create_superuser(
            username='test',
            email='a@a.com',
            password='test')
        self.client.force_authenticate(user=user)
        response = self.client.post('/games/')
        self.assertEqual(201, response.status_code)

        data = {'game': 1, 'field_num': 1}
        response = self.client.post('/turns/', data)
        self.assertEqual(201, response.status_code)
        # 'O' next turn
        self.assertEqual('O', response.data['client_data']['now_playing'])

        data = {'game': 1, 'field_num': 7}
        response = self.client.post('/turns/', data)
        self.assertEqual(201, response.status_code)
        # 'X' next turn
        self.assertEqual('X', response.data['client_data']['now_playing'])

        data = {'game': 1, 'field_num': 2}
        response = self.client.post('/turns/', data)
        self.assertEqual(201, response.status_code)

        data = {'game': 1, 'field_num': 8}
        response = self.client.post('/turns/', data)
        self.assertEqual(201, response.status_code)

        # Same field error
        data = {'game': 1, 'field_num': 8}
        response = self.client.post('/turns/', data)
        self.assertEqual(400, response.status_code)

        data = {'game': 1, 'field_num': 3}
        response = self.client.post('/turns/', data)
        self.assertEqual('X', response.data['client_data']['winner'])
        self.assertEqual(201, response.status_code)

        # No new moves after end
        data = {'game': 1, 'field_num': 6}
        response = self.client.post('/turns/', data)
        self.assertEqual(400, response.status_code)

        # Game's history, 5 turns
        response = self.client.get('/games/1/')
        self.assertEqual(5, len(response.data['misc_data']['turns']))
