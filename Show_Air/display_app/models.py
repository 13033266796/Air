from django.db import models

# Create your models here.
class AirInfo(models.Model):
    city_name = models.CharField(max_length=10)
    city_date = models.DateField()
    city_AQI = models.DecimalField(max_digits=18,decimal_places=2)
    city_PM2_5 = models.DecimalField(max_digits=18,decimal_places=2)

    def __str__(self):
        return self.city_name

class PredictInfo(models.Model):
    city_name = models.CharField(max_length=10)
    city_date = models.DateField()
    city_AQI = models.DecimalField(max_digits=18, decimal_places=2)
    city_PM2_5 = models.DecimalField(max_digits=18, decimal_places=2)

    def __str__(self):
        return self.city_name
