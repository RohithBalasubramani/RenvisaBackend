from django.db.models.signals import pre_save
from ecom1App.models import User

def updateUser(sender, instance, **kwargs):
    pass

pre_save.connect(updateUser, sender=User)