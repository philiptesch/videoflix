import subprocess
import os
from django.core.files import File

def convert_Video(video):
    target_dir = os.path.join('media', 'video', 'hls')
    os.makedirs(target_dir, exist_ok=True)
    target = os.path.join(target_dir, video.replace('.mp4', '_480.mp4'))
    ffmpeg_command = [
        '-i', video,
        '-s', 'hd480',
        '-c:v', 'libx264',
        '-crf', '23',
        '-c:a', 'aac',
        '-strict', '-2',
        target
    ]

    if ffmpeg(*ffmpeg_command):
        with open(target, 'rb') as resized_video:
            video.file.save(video, File(resized_video))
        os.remove(target)
        return video
    else:
        return None
    



def ffmpeg(*cmd):
  try:
    subprocess.check_output(['ffmpeg'] + list(cmd))
  except subprocess.CalledProcessError:
    return False
  return True