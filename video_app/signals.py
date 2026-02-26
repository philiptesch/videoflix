from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import  Video
import os
from .tasks import save_new_video_path

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created, **kwargs):

    print('Video was saved')
    if  created:
        print('New object created', instance.id)
    

        save_new_video_path(instance, instance.id)

        
        
        
@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, using, **kwargs):
    if instance.video_file:
        file_path = instance.video_file.path
        print('Video path found')
        
        if os.path.isfile(file_path):
            os.remove(file_path)
            print('Video was deleted from filesystem')
    else: 
        print('Fehler')        