from django.core.management.base import BaseCommand, CommandError
from hotelfinder.apps.hotelmanagement.services.hotelimporter import import_hotel_data, InvalidStatusCode
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)


class Command(BaseCommand):
    help = "Import hotel data"

    def handle(self, *args, **options):
        try:
            import_hotel_data()
            logging.info("Successfully imported hotel data")
        except InvalidStatusCode as status_code:
            logging.error(
                f"Received status code {status_code} during hotel import.")
            # raise CommandError(
            #     f"Received status code {status_code} during import.")
