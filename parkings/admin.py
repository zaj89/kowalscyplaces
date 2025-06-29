from django.contrib import admin
from parkings.models import Parking


@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ('name', 'coords', 'description')
    search_fields = ('name',)