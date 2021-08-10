from django.shortcuts import render

from .services.hotelimporter import import_hotel_data


def home(request):
    import_hotel_data()
    return render(request, "index.html")

# Create your views here.
