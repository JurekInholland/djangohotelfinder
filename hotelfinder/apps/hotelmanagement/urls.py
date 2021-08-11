from django.urls import path
from .views import (delete_city_view,
                    home,
                    hotel_finder_view,
                    admin_view,
                    add_city_view,
                    add_hotel_view,
                    edit_city_view,
                    edit_hotel_view,
                    login_view, logout_view,
                    delete_city_view,
                    delete_hotel_view)


urlpatterns = [
    path('', home, name="home"),
    path('hotels/', hotel_finder_view),
    path('hoteladmin/', admin_view, name="hadmin"),
    path('editcity/<str:code>', edit_city_view, name="editcity"),
    path('edithotel/<str:code>', edit_hotel_view, name="edithotel"),

    path('addcity/', add_city_view, name="addcity"),
    path('addhotel/', add_hotel_view, name="addhotel"),

    path('deletecity/<str:code>', delete_city_view, name="deletecity"),
    path('deletehotel/<str:code>', delete_hotel_view, name="deletehotel"),



    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),

]
