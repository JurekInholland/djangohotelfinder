import os
import csv
import codecs
import requests
from django.db import IntegrityError
from requests.models import HTTPBasicAuth
from ..models import City, Hotel

# This could be loaded from environment variables as well.
CITIES_URL = "http://rachel.maykinmedia.nl/djangocase/city.csv"
HOTELS_URL = "http://rachel.maykinmedia.nl/djangocase/hotel.csv"


def import_hotel_data():

    auth = HTTPBasicAuth(os.environ.get("HTTP_AUTH_USER"),
                         os.environ.get("HTTP_AUTH_PASS"))

    store_cities(load_csv(CITIES_URL, auth))
    store_hotels(load_csv(HOTELS_URL, auth))


def store_cities(cities: list):
    for city in cities:
        City.objects.get_or_create(code=city[0], name=city[1])


def store_hotels(hotels: list):
    for hotel in hotels:
        Hotel.objects.get_or_create(city=City.objects.get(
            code=hotel[0]), code=hotel[1], name=hotel[2])


def load_csv(url: str, auth: HTTPBasicAuth = None) -> list:
    res = requests.get(url, auth=auth)
    print("response status:", res.status_code)
    if res.status_code == 200:
        csv_content = csv.reader(codecs.iterdecode(
            res.iter_lines(), 'utf-8'), delimiter=';', quotechar='"')
        return list(csv_content)
    return []
