from django.contrib import admin
from .models import Trip, Booking, Review, Cart

admin.site.register(Trip)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Cart)