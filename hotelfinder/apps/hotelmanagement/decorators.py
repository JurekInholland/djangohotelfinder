from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import City, Hotel, CityManager
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render


def city_manager_exists(view_func):
    def wrapper_function(request, user_id):
        try:
            manager = CityManager.objects.get(user_id=user_id)
            return view_func(request, user_id)
        except CityManager.DoesNotExist:
            context = {"error": {"title": "City manager does not exist.",
                                 "message": f"The city manager with id {user_id} does not exist."}}
            return render(request, "error.html", context)
    return wrapper_function


def city_exists(view_func):
    def wrapper_function(request, code):
        try:
            city = City.objects.get(code=code)
            return view_func(request, code)
        except City.DoesNotExist:
            context = {"error": {"title": "City does not exist",
                                 "message": f"The city with code {code} does not exist."}}
            return render(request, "error.html", context)
    return wrapper_function


def hotel_exists(view_func):
    def wrapper_function(request, code):
        try:
            hotel = Hotel.objects.get(code=code)
            return view_func(request, code)
        except Hotel.DoesNotExist:
            context = {"error": {"title": "Hotel does not exist",
                                 "message": f"The hotel with code {code} does not exist."}}
            return render(request, "error.html", context)
    return wrapper_function


def is_city_manager(view_func):
    def wrapper_function(request, *args, **kwargs):
        try:
            if request.user.citymanager:
                return view_func(request)
        except ObjectDoesNotExist:
            context = {'error': {'title': 'Insufficient permissions',
                       'message': 'You are no city manager.'}}
            return render(request, "error.html", context)
    return wrapper_function


def is_manager_of_hotel(view_func):
    def wrapper_function(request, code, *args, **kwargs):
        try:
            hotel = Hotel.objects.get(code=code)
        except Hotel.DoesNotExist:
            context = {'error': {'title': 'Hotel does not exist',
                       'message': f'The hotel with code {code} does not exist.'}}
            return render(request, "error.html", context)

        try:
            if request.user.citymanager.city == hotel.city:
                # User is city manager of the hotel's city
                return view_func(request, code)
            else:
                context = {'error': {'title': 'Insufficient permissions',
                                     'message': f'You have no permission to modify hotels in {hotel.city}.'}}
        except ObjectDoesNotExist:
            context = {'error': {'title': 'Insufficient permissions',
                                 'message': 'You are no city manager.'}}
        return render(request, "error.html", context)
    return wrapper_function
