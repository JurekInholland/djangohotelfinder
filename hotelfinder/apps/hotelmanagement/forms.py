from django import forms
from .models import City, Hotel


class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = "__all__"


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = "__all__"
