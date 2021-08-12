from django.urls import path
from .views import (add_city_manager_view, delete_city_view,
                    home,
                    hotel_finder_view,
                    admin_view,
                    add_city_view,
                    add_hotel_view,
                    edit_city_view,
                    edit_hotel_view,
                    login_view, logout_view,
                    delete_city_view,
                    delete_hotel_view,
                    manage_city_view,
                    manage_edit_hotel_view,
                    manage_add_hotel_view,
                    manage_delete_hotel_view,
                    edit_city_manager_view,
                    delete_city_manager_view,
                    add_city_manager_view)


urlpatterns = [
    path('', home, name="home"),
    path('hotels/', hotel_finder_view, name="hotels"),
    path('hoteladmin/', admin_view, name="hadmin"),
    path('editcity/<str:code>', edit_city_view, name="editcity"),
    path('edithotel/<str:code>', edit_hotel_view, name="edithotel"),

    path('addcity/', add_city_view, name="addcity"),
    path('addhotel/', add_hotel_view, name="addhotel"),

    path('deletecity/<str:code>', delete_city_view, name="deletecity"),
    path('deletehotel/<str:code>', delete_hotel_view, name="deletehotel"),

    path('manage/', manage_city_view, name="manage"),
    path('manage/edit/<str:code>', manage_edit_hotel_view, name="manageedit"),
    path('manage/delete/<str:code>', manage_delete_hotel_view, name="managedelete"),
    path('manage/add/', manage_add_hotel_view, name="manageadd"),

    path('hoteladmin/editmanager/<str:user_id>',
         edit_city_manager_view, name="editmanager"),
    path('hoteladmin/deletemanager/<str:user_id>',
         delete_city_manager_view, name="deletemanager"),

    path('hoteladmin/addmanager/', add_city_manager_view, name="addmanager"),

    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
]
