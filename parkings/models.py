from django.db import models

from parkings.validators import validate_coordinates


def round_coords(coords):
    try:
        lat, lng = map(float, coords.split(','))
        return f"{round(lat, 6)},{round(lng, 6)}"
    except Exception:
        return coords

class Parking(models.Model):
    name = models.CharField(max_length=100, blank=True, verbose_name="Nazwa")
    coords = models.CharField(max_length=100, verbose_name="Współrzędne", validators=[validate_coordinates])  # format: "lat,lng"
    description = models.TextField(blank=True, verbose_name="Opis")
    source_location = models.ForeignKey('locations.Location', null=True, blank=True, on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        self.coords = round_coords(self.coords)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name or f"Parking ({self.coords})"
