import json
from rest_framework.test import APITestCase
from django.urls import reverse

from .models import Event


class EventTestCase(APITestCase):
    def setUp(self):
        self.event = Event.objects.create(date="2024-07-04", views=10, clicks=20, cost=1)

    def tearDown(self) -> None:
        self.event.delete()

    def test_event_create_view(self):
        """
        Проверка создания события через view events
        """
        post_data = {"date": "2024-07-04", "views": "20", "clicks": "20", "cost": "2"}
        post_data_json = json.dumps(post_data)
        response = self.client.post(
            reverse("apistatisticapp:events"), post_data_json, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(
            Event.objects.filter(date=post_data['date'], views=post_data['views'], clicks=post_data['clicks'],
                                 cost=post_data['cost']).exists())

    def test_event_delete_view(self):
        """
        Проверка удаления события через view events
        """
        Event.objects.create(date="2024-06-04", views="20", clicks=30, cost=3)
        response = self.client.delete(reverse("apistatisticapp:events"))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Event.objects.all().exists())

    def test_event_list_view(self):
        """
        Проверка отображения статистики, агрегированной по дате с дополнительными полями, сортировкой и выборкой по диапазону дат
        """
        Event.objects.create(date="2024-07-04", views=20, clicks=10, cost=5)
        Event.objects.create(date="2024-06-04", views=20, clicks=10, cost=5)
        query_params = {
            'from': '2024-06-01',
            'to': '2024-07-04',
            'ordering': 'date'
        }
        response = self.client.get(reverse("apistatisticapp:events"), data=query_params)
        self.assertEqual(response.status_code, 200)

        expected_data = [{"date": "2024-06-04", "views": 20, "clicks": 10, "cost": "5.00", "cpc": 0.5, "cpm": 250.0}, {
            "date": "2024-07-04", "views": 30, "clicks": 30, "cost": "6.00", "cpc": 0.2, "cpm": 200.0}]
        response_data = json.loads(response.content)  # Преобразуем контент ответа в словарь
        self.assertEqual(response_data, expected_data)
