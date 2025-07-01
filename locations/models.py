from django.db import models
from django.contrib.auth.models import User

from locations.validators import validate_coordinates


def round_coords(coords):
    try:
        lat, lng = map(float, coords.split(','))
        return f"{round(lat, 6)},{round(lng, 6)}"
    except Exception:
        return coords


class Location(models.Model):
    class Meta:
        verbose_name = "Punkt"
        verbose_name_plural = "Punkty"

    name = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    entry_coords = models.CharField(max_length=100)
    office_coords = models.CharField(max_length=100, blank=True, null=True)
    office_description = models.TextField(blank=True, null=True)
    loading_coords = models.CharField(max_length=100, blank=True, null=True)
    loading_description = models.TextField(blank=True, null=True)
    night_unloading = models.BooleanField(default=False)
    night_unloading_description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.town})"

class Parking(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nazwa")
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True, related_name="parkings")
    coords = models.CharField(max_length=100, verbose_name="Współrzędne", validators=[validate_coordinates])
    description = models.TextField(blank=True, null=True, verbose_name="Opis")

    def __str__(self):
        return f"Parking ({self.coords}) przy {self.location.name}"

    def save(self, *args, **kwargs):
        self.coords = round_coords(self.coords)
        super().save(*args, **kwargs)
