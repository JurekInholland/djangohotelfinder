from django.db import models


class City(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=120)

    def natural_key(self):
        return {"code": self.code, "name": self.name}

    def __str__(self):
        return self.name


class Hotel(models.Model):
    code = models.CharField(max_length=6, unique=True)
    name = models.CharField(max_length=120)
    city = models.ForeignKey(City, on_delete=models.deletion.CASCADE)

    def __str__(self):
        return self.name
