from django import forms
from .models import City, CityManager, Hotel


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = "__all__"


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = "__all__"


class CityManagerForm(forms.ModelForm):
    class Meta:
        model = CityManager
        fields = "__all__"


class ManagerHotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ["code", "name"]
