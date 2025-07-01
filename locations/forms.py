from django import forms
from .models import Location, Parking

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = [
            'name', 'town', 'entry_coords',
            'office_coords', 'office_description',
            'loading_coords', 'loading_description',
            'night_unloading', 'night_unloading_description',
        ]

class ParkingForm(forms.ModelForm):
    class Meta:
        model = Parking
        fields = ['name', 'coords', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }
