import subprocess
import os
from django.core.files import File


def save_new_video_path(instance, id):
    old_path = instance.video_file.path 
    new_name = f"new_video_name_{id}.mp4"
    old = os.path.dirname(old_path)
    new_path = os.path.join(old, new_name)
    os.rename(old_path, new_path)
    convert_Video(instance, new_path, new_name)


def convert_Video(instance, new_path, new_name):
    target_dir = os.path.join('media', 'video', 'hls')
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, new_name.replace('.mp4', '_480.mp4'))
    ffmpeg_command = [
        '-i', new_path,
        '-s', 'hd480',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        target
    ]

    if ffmpeg(*ffmpeg_command):
        with open(new_path, 'rb') as f : 
            instance.video_file.save(os.path.basename(new_path), File(f), 
            save=True )
        return target
    
    else:
        return None
    



def ffmpeg(*cmd):
    try:
        subprocess.run(['ffmpeg'] + list(cmd), check=True)
    except subprocess.CalledProcessError:
        return False
    return True