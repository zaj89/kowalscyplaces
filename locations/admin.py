from django.contrib import admin
from .models import Location, Parking

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'town', 'entry_coords', 'created_by')
    search_fields = ('name', 'town')

@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ('name', 'coords', 'description')
    search_fields = ('name',)