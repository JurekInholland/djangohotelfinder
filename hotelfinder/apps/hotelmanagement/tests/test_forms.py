from django.test.testcases import TestCase, Client
from django.contrib.auth.models import User

from ..forms import CityForm, CityManagerForm, HotelForm, ManagerHotelForm
from ..models import City


class TestForms(TestCase):

    def test_city_form_valid_data(self):
        form = CityForm(data={
            'code': 'ABC',
            'name': 'TestName'
        })
        self.assertTrue(form.is_valid())

    def test_city_form_no_data(self):
        form = CityForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_city_invalid_data(self):
        form = CityForm(data={
            'code': 'code_longer_than_3_chars',
            'name': ''
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_hotel_form_valid_data(self):
        city = City.objects.create(code='ABC', name='test city')
        form = HotelForm(data={
            'code': 'ABCD',
            'name': 'Test Hotel',
            'city': city})
        self.assertTrue(form.is_valid())

    def test_hotel_form_no_data(self):
        form = HotelForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_hotel_form_invalid_data(self):
        form = HotelForm(data={
            'code': 'code_longer_than_6_chars',
            'name': '',
            'city': 123
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_citymanager_form_valid_data(self):
        city = City.objects.create(code='ABC', name='test city')
        user = User(username='user', email='user@email.com')
        user.save()
        form = CityManagerForm(data={
            'user': user,
            'city': city
        })
        self.assertTrue(form.is_valid())

    def test_citymanager_form_no_data(self):
        form = CityManagerForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_citymanager_form_invalid_data(self):
        form = CityManagerForm(data={
            'user': 'invalid',
            'city': 123
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_managerhotel_form_valid_data(self):
        form = ManagerHotelForm(data={
            'code': 'ABC',
            'name': 'Test Name'
        })
        self.assertTrue(form.is_valid())

    def test_managerhotel_form_no_data(self):
        form = ManagerHotelForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_managerhotel_invalid_data(self):
        form = ManagerHotelForm(data={
            'code': 'code_longer_than_3_chars',
            'name': ''
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)
