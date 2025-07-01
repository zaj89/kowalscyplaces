from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Location, Parking
from .forms import LocationForm, ParkingForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.forms import inlineformset_factory

@login_required
def index(request):
    return render(request, 'locations/index.html')

@login_required
def search_locations(request):
    query = request.GET.get('q', '')
    results = Location.objects.filter(Q(town__icontains=query) | Q(name__icontains=query)).values('id', 'name', 'town')
    return JsonResponse(list(results), safe=False)

@login_required
def location_detail(request, location_id):
    location = get_object_or_404(Location, id=location_id)

    parking_data = []
    for i in range(1, 6):
        coord = getattr(location, f'parking{i}_coords', None)
        description = getattr(location, f'parking{i}_description', '')
        if coord:
            parking_data.append({
                'number': i,
                'coords': coord,
                'description': description,
            })

    return render(request, 'locations/detail.html', {
        'location': location,
        'parking_data': parking_data
    })

ParkingFormSet = inlineformset_factory(Location, Parking, form=ParkingForm, extra=0, can_delete=True)

@login_required
def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        formset = ParkingFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            location = form.save(commit=False)
            location.created_by = request.user
            location.save()
            formset.instance = location
            formset.save()
            messages.success(request, "Punkt i parkingi zostały dodane.")
            return redirect('index')
        else:
            messages.error(request, "Błąd w formularzu punktu lub parkingów.")
    else:
        form = LocationForm()
        formset = ParkingFormSet()

    return render(request, 'locations/add_location.html', {'form': form, 'formset': formset})

@login_required
def edit_location(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    if request.method == 'POST':
        form = LocationForm(request.POST, instance=location)
        formset = ParkingFormSet(request.POST, instance=location)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Punkt i parkingi zostały zaktualizowane.")
            return redirect('location_detail', location_id=location.id)
        else:
            messages.error(request, "Błąd w formularzu punktu lub parkingów.")
    else:
        form = LocationForm(instance=location)
        formset = ParkingFormSet(instance=location)

    return render(request, 'locations/edit_location.html', {'form': form, 'formset': formset, 'location': location})


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