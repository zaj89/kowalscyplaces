from django.contrib import admin
from .models import Location, Parking

class ParkingInline(admin.TabularInline):
    model = Parking
    fk_name = 'location'  # nazwa FK w modelu Parking
    extra = 0

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'town', 'created_by']
    inlines = [ParkingInline]

@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'coords']