from django.contrib import admin
from .models import Location

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'town', 'entry_coords', 'created_by')
    search_fields = ('name', 'town')