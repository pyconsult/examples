from django.db import models

# Create your models here.


class Owner(models.Model):
    """
    Generic owner
    """
    name = models.CharField(
            max_length=40,
            )

class Car(models.Model):
    """
    Simple Car model
    """
    license_plate = models.CharField(
            max_length=20,
            )
    owner = models.ForeignKey(
            Owner,
            related_name='car',
            )
     
class Motorcycle(models.Model):
    """
    Simple Motorcycle model
    """
    license_plate = models.CharField(
            max_length=20,
            )
    owner = models.ForeignKey(
            Owner,
            )
    
class Trailer(models.Model):
    """
    Simple Trailer model
    """
    license_plate = models.CharField(
            max_length=20,
            )
    car = models.ForeignKey(
            Car,
            related_name='trailer',
            )
    weight = models.DecimalField(
            max_digits=6,
            decimal_places=2,
            )

        
        
