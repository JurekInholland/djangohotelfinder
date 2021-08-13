from django.test.testcases import TestCase
from django.contrib.auth.models import User

from ..models import City, CityManager, Hotel


class TestModels(TestCase):
    def setUp(self):
        self.city = City.objects.create(code="ABC", name="TestCity")
        self.hotel = Hotel.objects.create(
            code="ABC1", name="TestHotel", city=self.city)

    def test_city_model(self):
        self.assertEquals(self.hotel.city, self.city)

    def test_city_manager_model(self):
        user = User.objects.create(username="user", email="user@email.com")
        user.set_password("password")
        user.save()
        manager = CityManager.objects.create(user=user, city=self.city)
        self.assertEquals(manager.city, self.city)
