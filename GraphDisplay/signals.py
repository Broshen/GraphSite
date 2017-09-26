from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_delete

from .models import ResultFile

@receiver(post_delete, sender=ResultFile)
def on_delete(sender, **kwargs):
    instance = kwargs['instance']
    # ref is the name of the field file of the Car model
    # replace with name of your file field
    instance.file.delete(save=False)