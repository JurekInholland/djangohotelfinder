# DjangoHotelFinder

A live demo can be found [here](https://djangohotelfinder.herokuapp.com/)

# To start developing

To run manage.py within the container:
`docker exec -it hotelmanager python3 manage.py`

### First time setup

- clone this repo
- supply http auth user and password for the cronjob in docker.compose.yml
- run `docker-compose up --build` to start python django & cron containers
- run `docker exec -it hotelmanager python3 manage.py migrate` to apply migrations.
- run `docker exec -it cron python3 manage.py import_hotel_data` to import data instantly instead of waiting for the daily cronjob.

### To run tests:

- `docker exec -it hotelmanager python3 manage.py collectstatic`
- `docker exec -it hotelmanager python3 manage.py test hotelfinder.apps.hotelmanagement.tests`
