from django.shortcuts import render
from django.core import serializers
from django.http import HttpResponse, JsonResponse

from .services.hotelimporter import import_hotel_data
from .models import City, Hotel


def hotel_finder_view(request):
    if request.method == 'POST':
        city_name = request.POST.get("name")

        hotels = Hotel.objects.filter(
            city__name__startswith=city_name).order_by("name")

        # Return no more than 99 hotels
        if (len(hotels) > 99):
            hotels = hotels[0:99]

        json = serializers.serialize(
            'json', hotels, use_natural_foreign_keys=True, use_natural_primary_keys=True)
        return JsonResponse(json, safe=False)

    return HttpResponse()


def home(request):
    import_hotel_data()
    context = {}
    context["city_list"] = City.objects.all()
    return render(request, "index.html", context)

# Create your views here.
