from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime

class Trip(models.Model):
    id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    duration_days = models.IntegerField()
    image = models.ImageField(null=True, blank=True, upload_to="trips/")
    location = models.CharField(max_length=255)

class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    trips = models.ManyToManyField(Trip)
    nr_trips = models.IntegerField(default=0)
    total = models.FloatField()
    booking_details = models.CharField(max_length=255)
    date = models.DateTimeField(default=datetime.now, blank=True)

    def get_trips(self):
        return self.trips.all()

class Review(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(default=1, validators=[
                                MinValueValidator(1), MaxValueValidator(5)])
    content = models.CharField(max_length=255)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.trip.name} in cart"