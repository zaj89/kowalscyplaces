from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Parking
from .forms import ParkingForm

def parking_map(request):
    parkings = Parking.objects.all()
    form = ParkingForm()
    return render(request, 'parkings/parking_map.html', {'parkings': parkings, 'form': form})

@login_required
def add_parking(request):
    if request.method == 'POST':
        form = ParkingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Parking został dodany.")
            return redirect('parking_map')
        else:
            messages.error(request, "Wystąpił błąd podczas dodawania parkingu.")
    else:
        form = ParkingForm()

    return render(request, 'parkings/add_parking.html', {'form': form})