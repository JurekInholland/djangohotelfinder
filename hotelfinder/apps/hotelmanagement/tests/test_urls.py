from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import (home,
                     hotel_finder_view,
                     admin_view,
                     edit_city_view,
                     edit_hotel_view,
                     add_city_view,
                     add_hotel_view,
                     delete_city_view,
                     delete_hotel_view,
                     manage_city_view,
                     manage_edit_hotel_view,
                     manage_delete_hotel_view,
                     manage_add_hotel_view,
                     edit_city_manager_view,
                     delete_city_manager_view,
                     add_city_manager_view)


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home)

    def test_hotels_url_is_resolved(self):
        url = reverse('hotels')
        self.assertEquals(resolve(url).func, hotel_finder_view)

    def test_admin_url_is_resolved(self):
        url = reverse('hadmin')
        self.assertEquals(resolve(url).func, admin_view)

    def test_editcity_url_is_resolved(self):
        url = reverse("editcity", args=["ABC"])
        self.assertEquals(resolve(url).func, edit_city_view)

    def test_edithotel_url_is_resolved(self):
        url = reverse("edithotel", args=["ABC"])
        self.assertEquals(resolve(url).func, edit_hotel_view)

    def test_addcity_url_is_resolved(self):
        url = reverse("addcity")
        self.assertEquals(resolve(url).func, add_city_view)

    def test_addhotel_url_is_resolved(self):
        url = reverse("addhotel")
        self.assertEquals(resolve(url).func, add_hotel_view)

    def test_deletecity_url_is_resolved(self):
        url = reverse("deletecity", args=["ABC"])
        self.assertEquals(resolve(url).func, delete_city_view)

    def test_deletehotel_url_is_resolved(self):
        url = reverse("deletehotel", args=["ABC"])
        self.assertEquals(resolve(url).func, delete_hotel_view)

    def test_manage_url_is_resolved(self):
        url = reverse("manage")
        self.assertEquals(resolve(url).func, manage_city_view)

    def test_manage_edit_url_is_resolved(self):
        url = reverse("manageedit", args=["ABC"])
        self.assertEquals(resolve(url).func, manage_edit_hotel_view)

    def test_manage_delete_url_is_resolved(self):
        url = reverse("managedelete", args=["ABC"])
        self.assertEquals(resolve(url).func, manage_delete_hotel_view)

    def test_manage_add_url_is_resolved(self):
        url = reverse("manageadd")
        self.assertEquals(resolve(url).func, manage_add_hotel_view)

    def test_edit_manager_url_is_resolved(self):
        url = reverse("editmanager", args=[1])
        self.assertEquals(resolve(url).func, edit_city_manager_view)

    def test_delete_manager_url_is_resolved(self):
        url = reverse("deletemanager", args=["ABC"])
        self.assertEquals(resolve(url).func, delete_city_manager_view)

    def test_manage_add_url_is_resolved(self):
        url = reverse("addmanager")
        self.assertEquals(resolve(url).func, add_city_manager_view)
