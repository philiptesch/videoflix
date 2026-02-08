from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def create_lecture(sender, instance, created, **kwargs):
    if  created:
        print('New object created')