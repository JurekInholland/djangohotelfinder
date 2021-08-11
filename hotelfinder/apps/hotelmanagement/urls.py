from django.urls import path
from .views import home, hotel_finder_view


urlpatterns = [
    path('', home, name="home"),
    path('hotels/', hotel_finder_view)
]
