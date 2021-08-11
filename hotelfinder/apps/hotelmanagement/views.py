from django.shortcuts import redirect, render
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required

from requests import auth

from .services.hotelimporter import import_hotel_data
from .models import City, Hotel
from .forms import CityForm, HotelForm


def logout_view(request):
    logout(request)
    return redirect("home")


def login_view(request):
    context = {}

    if request.method == "POST":

        user = authenticate(username=request.POST.get(
            "name"), password=request.POST.get(
            "password"))
        if user is not None:
            login(request, user)
            print("successful login")
            context["feedback"] = "SUCCESS"

            redirect_to = "/"
            nxt = request.GET.get("next")
            if nxt:
                redirect_to = nxt
            return redirect(redirect_to)

        else:
            context["feedback"] = "Username or password is incorrect."
            print("user not found")
        print("LOGIN DATA:", request.POST.get(
            "name"), request.POST.get("password"))

    if request.user.is_authenticated:
        context["feedback"] = "You are already logged in"

    return render(request, "login.html", context)


@staff_member_required(login_url='/login')
def delete_hotel_view(request, code=None):
    hotel = Hotel.objects.get(code=code)
    if request.method == "POST":
        hotel.delete()
        return redirect("hadmin")
    context = {"object": hotel, "object_type": "hotel"}
    return render(request, "deleteobject.html", context)


@staff_member_required(login_url='/login')
def delete_city_view(request, code=None):
    city = City.objects.get(code=code)
    if request.method == "POST":
        city.delete()
        return redirect("hadmin")
    context = {"object": city, "object_type": "city"}
    return render(request, "deleteobject.html", context)


@staff_member_required(login_url='/login')
def add_city_view(request):
    if request.method == "POST":
        form = CityForm(request.POST or None)
        if form.is_valid():
            form.save()
            return redirect("hadmin")

    context = {"form": CityForm(), "headline": "Add city"}
    return render(request, "editobject.html", context)


@staff_member_required(login_url='/login')
def add_hotel_view(request):
    if request.method == "POST":
        form = HotelForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("hadmin")

    context = {"form": HotelForm(), "headline": "Add hotel"}
    return render(request, "editobject.html", context)


@staff_member_required(login_url='/login')
def edit_hotel_view(request, code=None):
    if request.method == "POST":
        form = HotelForm(request.POST or None,
                         instance=Hotel.objects.get(code=code))
        if form.is_valid():
            form.save()
            return redirect("hadmin")

    context = {"form": HotelForm(
        request.POST or None, instance=Hotel.objects.get(code=code)),
        "headline": "Edit Hotel"}

    return render(request, "editobject.html", context)


@staff_member_required(login_url='/login')
def edit_city_view(request, code=None):
    if request.method == "POST":
        form = CityForm(request.POST or None,
                        instance=City.objects.get(code=code))
        if form.is_valid():
            form.save()
            return redirect("hadmin")

    context = {"form": CityForm(
        request.POST or None, instance=City.objects.get(code=code)),
        "headline": "Edit City"}
    return render(request, "editobject.html", context)


@staff_member_required(login_url='/login')
def admin_view(request):

    perms = request.user.get_user_permissions()
    print("PERMS:")
    print(perms)
    context = {"hotels": Hotel.objects.all(), "cities": City.objects.all}
    return render(request, "admin.html", context)


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
    # import_hotel_data()
    context = {}
    context["city_list"] = City.objects.all()
    return render(request, "index.html", context)

# Create your views here.
