from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Location
from parkings.models import Parking

@receiver(post_save, sender=Location)
def create_parkings_from_location(sender, instance, **kwargs):
    for i in range(1, 6):
        coords = getattr(instance, f"parking{i}_coords", None)
        desc = getattr(instance, f"parking{i}_description", "")
        if coords:
            Parking.objects.get_or_create(
                coords=coords,
                source_location=instance,
                defaults={'description': desc, 'name': f"Parking {i} przy {instance.name}"}
            )
