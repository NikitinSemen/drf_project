from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course
from users.models import User, Subscription


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="user_1@test.ru")
        self.course = Course.objects.create(name='Курс обществознания',
                                            description='Курс направлен на изучение основ права')
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        url = reverse('users:subscribe')
        data = {
            'course_id': self.course.id
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )

