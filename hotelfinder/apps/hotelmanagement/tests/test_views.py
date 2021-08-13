
from collections import namedtuple
from django.db.models import manager
from django.http import response
from django.test.testcases import TestCase, Client
from django.contrib.auth.models import User

from django.urls import reverse
from ..models import City, CityManager, Hotel


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

        self.city = City.objects.create(code="TES", name="TestCity")
        self.hotel = Hotel.objects.create(
            city=self.city, code="TES01", name="TestHotel")

    def setup_staff_user(self):
        staff_user = User(username='user', email='user@email.com')
        staff_user.set_password("password")
        staff_user.is_staff = True
        staff_user.save()
        self.client.login(username="user",
                          password="password")

    def setup_city_manager_user(self):
        user = User(username='manager', email='manager@email.com')
        user.set_password("password")
        user.save()

        self.client.login(username="manager",
                          password="password")
        manager = CityManager(user=user, city=self.city)
        manager.save()
        return manager

    def test_home_GET(self):
        response = self.client.get(reverse("home"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_login_GET(self):
        response = self.client.get(reverse("login"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_logout_GET(self):
        response = self.client.get(reverse("logout"))
        self.assertEquals(response.status_code, 302)

    def test_admin_GET(self):
        self.setup_staff_user()

        response = self.client.get(reverse("hadmin"), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin.html')

    def test_editcity_GET(self):
        self.setup_staff_user()

        response = self.client.get(
            reverse("editcity", args=[self.city.code]), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'editobject.html')

    def test_edithotel_GET(self):
        self.setup_staff_user()

        response = self.client.get(
            reverse("edithotel", args=[self.hotel.code]), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'editobject.html')

    def test_addcity_GET(self):
        self.setup_staff_user()
        response = self.client.get(
            reverse("addcity"), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'editobject.html')

    def test_addhotel_GET(self):
        self.setup_staff_user()
        response = self.client.get(
            reverse("addhotel"), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'editobject.html')

    def test_deletecity_GET(self):
        self.setup_staff_user()
        response = self.client.get(
            reverse("deletecity", args=[self.city.code]), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'deleteobject.html')

    def test_deletehotel_GET(self):
        self.setup_staff_user()
        response = self.client.get(
            reverse("deletehotel", args=[self.hotel.code]), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'deleteobject.html')

    def test_edit_city_manager_GET(self):
        manager_user = self.setup_city_manager_user()
        self.setup_staff_user()

        response = self.client.get(
            reverse("editmanager", args=[manager_user.user_id]), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'editobject.html')

    def test_add_city_manager_GET(self):
        self.setup_staff_user()
        response = self.client.get(
            reverse("addmanager"), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'editobject.html')

    def test_delete_city_manager_GET(self):
        manager_user = self.setup_city_manager_user()
        self.setup_staff_user()

        response = self.client.get(
            reverse("deletemanager", args=[manager_user.user_id]), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'deleteobject.html')

    def test_manage_city_GET(self):
        self.setup_city_manager_user()
        response = self.client.get(reverse("manage"), follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'managecity.html')

    def test_manage_edit_hotel_GET(self):
        self.setup_city_manager_user()
        response = self.client.get(
            reverse("manageedit", args=[self.hotel.code]), follow=True)    # def test_edit_city_manager_GET(self):
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'editobject.html')

    def test_manage_delete_hotel_GET(self):
        self.setup_city_manager_user()
        response = self.client.get(
            reverse("managedelete", args=[self.hotel.code]), follow=True)    # def test_edit_city_manager_GET(self):
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'deleteobject.html')

    def test_manage_add_hotel_GET(self):
        self.setup_city_manager_user()
        response = self.client.get(
            reverse("manageadd"), follow=True)    # def test_edit_city_manager_GET(self):
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'editobject.html')
