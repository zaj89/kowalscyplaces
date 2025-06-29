from django import forms
from .models import Parking

class ParkingForm(forms.ModelForm):
    class Meta:
        model = Parking
        fields = ['name', 'coords', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }
