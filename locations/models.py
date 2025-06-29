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

    name = models.CharField(max_length=100, verbose_name='Nazwa')
    town = models.CharField(max_length=100, verbose_name='Miejscowość')
    entry_coords = models.CharField(max_length=50, verbose_name='Współrzędne bramy wjazdowej', validators=[validate_coordinates])
    office_coords = models.CharField(max_length=50, blank=True, null=True, verbose_name='Współrzędne biura', validators=[validate_coordinates])
    office_description = models.TextField(blank=True, null=True, verbose_name='Opis biura')
    loading_coords = models.CharField(max_length=50, blank=True, null=True, verbose_name='Współrzędne załadunku/rozładunku', validators=[validate_coordinates])
    loading_description = models.TextField(blank=True, null=True, verbose_name='Opis załadunku/rozładunku')
    parking1_coords = models.CharField(max_length=50, blank=True, null=True, verbose_name='Współrzędne parkingu 1', validators=[validate_coordinates])
    parking1_description = models.TextField(blank=True, null=True, verbose_name='Opis parkingu 1')
    parking2_coords = models.CharField(max_length=50, blank=True, null=True, verbose_name='Współrzędne parkingu 2', validators=[validate_coordinates])
    parking2_description = models.TextField(blank=True, null=True, verbose_name='Opis parkingu 2')
    parking3_coords = models.CharField(max_length=50, blank=True, null=True, verbose_name='Współrzędne parkingu 3', validators=[validate_coordinates])
    parking3_description = models.TextField(blank=True, null=True, verbose_name='Opis parkingu 3')
    parking4_coords = models.CharField(max_length=50, blank=True, null=True, verbose_name='Współrzędne parkingu 4', validators=[validate_coordinates])
    parking4_description = models.TextField(blank=True, null=True, verbose_name='Opis parkingu 4')
    parking5_coords = models.CharField(max_length=50, blank=True, null=True, verbose_name='Współrzędne parkingu 5', validators=[validate_coordinates])
    parking5_description = models.TextField(blank=True, null=True, verbose_name='Opis parkingu 5')
    night_unloading = models.BooleanField(default=False, verbose_name='Rozładunek nocny')
    night_unloading_description = models.TextField(blank=True, null=True, verbose_name='Opis rozładunku nocnego')

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.entry_coords = round_coords(self.entry_coords)
        if self.office_coords:
            self.office_coords = round_coords(self.office_coords)
        if self.loading_coords:
            self.loading_coords = round_coords(self.loading_coords)
        if self.parking1_coords:
            self.parking1_coords = round_coords(self.parking1_coords)
        if self.parking2_coords:
            self.parking2_coords = round_coords(self.parking2_coords)
        if self.parking3_coords:
            self.parking3_coords = round_coords(self.parking3_coords)
        if self.parking4_coords:
            self.parking4_coords = round_coords(self.parking4_coords)
        if self.parking5_coords:
            self.parking5_coords = round_coords(self.parking5_coords)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.town})"
