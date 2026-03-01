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


def convert_Video(id, new_path, new_name):
    target_dir = os.path.join('media', 'video', '480p', str(id))
    os.makedirs(target_dir, exist_ok=True)
    playlist_path = os.path.join(target_dir, "index.m3u8")
    segment_path = os.path.join(target_dir, "segment_%03d.ts")

    ffmpeg_command = [
        '-i', new_path,
        '-vf', 'scale=854:480',      # 480p
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-f', 'hls',
        '-hls_time', '6',
        '-hls_playlist_type', 'vod',
        '-hls_segment_filename', segment_path,
        playlist_path
    ]
    if ffmpeg(*ffmpeg_command):
        return playlist_path
    else:
        return None
    



def ffmpeg(*cmd):
    try:
        subprocess.run(['ffmpeg'] + list(cmd), check=True)
    except subprocess.CalledProcessError:
        return False
    return True