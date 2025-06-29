from django.core.exceptions import ValidationError
import re

def validate_coordinates(value):
    # Dopuszcza format: np. 50.1234567890123,19.1234567890123 (do 13 miejsc po przecinku)
    pattern = r'^-?\d+(\.\d{1,18})?\s*,\s*-?\d+(\.\d{1,18})?$'
    if not re.match(pattern, value):
        raise ValidationError("Nieprawidłowy format. Użyj: '50.12345,19.12345' (do 18 miejsc po przecinku)")

    try:
        lat, lng = map(float, value.split(','))
        if not (-90 <= lat <= 90):
            raise ValidationError("Szerokość geograficzna (latitude) musi być w zakresie od -90 do 90.")
        if not (-180 <= lng <= 180):
            raise ValidationError("Długość geograficzna (longitude) musi być w zakresie od -180 do 180.")
    except ValueError:
        raise ValidationError("Współrzędne muszą być liczbami zmiennoprzecinkowymi oddzielonymi przecinkiem.")
