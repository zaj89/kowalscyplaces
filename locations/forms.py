from django import forms
from .models import Location

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = [
            'name', 'town', 'entry_coords',
            'office_coords', 'office_description',
            'loading_coords', 'loading_description',
            'parking1_coords', 'parking1_description',
            'parking2_coords', 'parking2_description',
            'parking3_coords', 'parking3_description',
            'parking4_coords', 'parking4_description',
            'parking5_coords', 'parking5_description',
            'night_unloading', 'night_unloading_description',
        ]
