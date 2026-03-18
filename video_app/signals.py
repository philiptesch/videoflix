from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import  Video
import os
from .tasks import save_new_video_path
from django_rq.queues import get_queue


@receiver(post_save, sender=Video, dispatch_uid="signal=uid")
def video_post_save(sender, instance, created, **kwargs):
    """
    Signal handler executed after a Video instance is saved.

    Behavior:
        - Triggered for every save() call on Video instances.
        - Prints a message confirming the save.
        - If the instance is newly created (created=True):
            - Prints the new object ID.
            - Calls save_new_video_path() task to process the new video file.
            - Optional: can enqueue the task in a Redis queue using django_rq (commented out).

    Args:
        sender (Model): The model class that triggered the signal (Video).
        instance (Video): The actual instance being saved.
        created (bool): True if a new object was created; False if updated.
        **kwargs: Additional signal keyword arguments.
    """

    print('Video was saved')
    if  created:
        print('New object created', instance.id)
    
        queue = get_queue('default', autocommit=True)
        queue.enqueue(save_new_video_path, instance, instance.id)
        
        
        
@receiver(post_delete, sender=Video)
def video_post_delete(sender, instance, using, **kwargs):
    """
    Signal handler executed after a Video instance is deleted.

    Behavior:
        - Checks if the instance had a video_file.
        - If the file exists on the filesystem, deletes it.
        - Prints debug messages for successful deletion or errors.

    Args:
        sender (Model): The model class that triggered the signal (Video).
        instance (Video): The actual instance being deleted.
        using (str): Database alias used.
        **kwargs: Additional signal keyword arguments.
    """
    
    if instance.video_file:
        file_path = instance.video_file.path
        print('Video path found')
        
        if os.path.isfile(file_path):
            os.remove(file_path)
            print('Video was deleted from filesystem')
    else: 
        print('Fehler')        