from django.core.management.base import BaseCommand, CommandError
from hotelfinder.apps.hotelmanagement.services.hotelimporter import import_hotel_data


class Command(BaseCommand):
    help = "Import hotel data"

    def handle(self, *args, **options):
        try:
            import_hotel_data()
        except:
            raise CommandError("Failed to import data.")
