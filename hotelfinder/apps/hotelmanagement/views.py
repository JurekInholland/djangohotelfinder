from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .models import City, CityManager, Hotel
from .forms import CityForm, HotelForm, ManagerHotelForm, CityManagerForm
from .decorators import is_manager_of_hotel, is_city_manager, hotel_exists, city_exists, city_manager_exists


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

            redirect_to = "/"
            nxt = request.GET.get("next")
            if nxt:
                redirect_to = nxt
            return redirect(redirect_to)
        else:
            context["feedback"] = "Username or password is incorrect."

    return render(request, "login.html", context)


@staff_member_required(login_url='/login')
@hotel_exists
def delete_hotel_view(request, code=None):
    hotel = Hotel.objects.get(code=code)
    if request.method == "POST":
        hotel.delete()
        return redirect("hadmin")

    context = {"object": hotel, "object_type": "hotel"}
    return render(request, "deleteobject.html", context)


@city_exists
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
    form = CityForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("hadmin")

    context = {"form": form, "headline": "Add city"}
    return render(request, "editobject.html", context)


@staff_member_required(login_url='/login')
def add_hotel_view(request):
    form = HotelForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("hadmin")

    context = {"form": form, "headline": "Add hotel"}
    return render(request, "editobject.html", context)


@staff_member_required(login_url='/login')
@hotel_exists
def edit_hotel_view(request, code=None):
    form = HotelForm(request.POST or None,
                     instance=Hotel.objects.get(code=code))

    if request.method == "POST":

        if form.is_valid():
            form.save()
            return redirect("hadmin")

    context = {"form": form,
               "headline": "Edit Hotel"}
    return render(request, "editobject.html", context)


@staff_member_required(login_url='/login')
@city_exists
def edit_city_view(request, code: str = None):
    form = CityForm(request.POST or None,
                    instance=City.objects.get(code=code))
    if request.method == "POST":
        form = CityForm(request.POST or None,
                        instance=City.objects.get(code=code))
        if form.is_valid():
            form.save()
            return redirect("hadmin")

    context = {"form": form,
               "headline": "Edit City"}
    return render(request, "editobject.html", context)


@staff_member_required(login_url='/login')
def edit_city_manager_view(request, user_id=None):
    form = CityManagerForm(
        request.POST or None, instance=CityManager.objects.get(user_id=user_id))

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("hadmin")

    context = {"form": form}
    return render(request, "editobject.html", context)


@staff_member_required(login_url='/login')
def add_city_manager_view(request):
    form = CityManagerForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("hadmin")

    context = {"form": form, "headline": "Add city manager"}
    return render(request, "editobject.html", context)


@staff_member_required(login_url='/login')
@city_manager_exists
def delete_city_manager_view(request, user_id=None):
    manager = CityManager.objects.get(user_id=user_id)

    if request.method == "POST":
        manager.delete()
        return redirect("hadmin")

    user = {"name": manager.user.username}
    context = {"object": user, "object_type": "City manager"}
    return render(request, "deleteobject.html", context)


@staff_member_required(login_url='/login')
def admin_view(request):

    context = {"hotels": Hotel.objects.all().order_by('code'), "cities": City.objects.all().order_by('code'),
               "managers": CityManager.objects.all().order_by("user_id")}
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

    context = {"error": {"title": "City was not specified.",
                         "message": "You have to specify a city via POST request to search for hotels."}}
    return render(request, "error.html", context)


@login_required(login_url='/login')
@is_manager_of_hotel
def manage_delete_hotel_view(request, code=None):
    hotel = Hotel.objects.get(code=code)

    if request.method == "POST":
        hotel.delete()
        return redirect("manage")

    context = {"object": hotel, "object_type": "hotel"}
    return render(request, "deleteobject.html", context)


@login_required(login_url='/login')
@is_manager_of_hotel
def manage_edit_hotel_view(request, code=None):

    hotel = Hotel.objects.get(code=code)
    form = ManagerHotelForm(request.POST or None,
                            instance=hotel)
    if request.method == "POST":

        if form.is_valid():
            hotel_form = form.save(commit=False)
            manager = CityManager.objects.get(user=request.user)
            hotel_form.city = manager.city
            hotel_form.save()
            return redirect('manage')

    context = {"form": form, "headline": "Edit Hotel"}
    return render(request, "editobject.html", context)


@login_required(login_url='/login')
@is_city_manager
def manage_add_hotel_view(request):

    if request.method == "POST":
        form = ManagerHotelForm(request.POST or None)
        if form.is_valid():
            hotel = form.save(commit=False)
            manager = CityManager.objects.get(user=request.user)
            hotel.city = manager.city
            hotel.save()
            return redirect('manage')
    form = ManagerHotelForm()
    context = {"form": form, "headline": "Add Hotel"}
    return render(request, "editobject.html", context)


@login_required(login_url='/login')
@is_city_manager
def manage_city_view(request):
    manager = CityManager.objects.get(user=request.user)
    city = manager.city
    hotels = Hotel.objects.filter(city=city).order_by("code")
    context = {"hotels": hotels, "city": city}
    return render(request, "managecity.html", context)


def home(request):
    context = {'city_list': City.objects.all()}
    return render(request, "index.html", context)
