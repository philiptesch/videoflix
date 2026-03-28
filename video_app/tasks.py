import subprocess
import os
from django.core.files import File

resolutions = [("480", "480p"), ("720", "720p"), ("1080", "1080p")]

def save_new_video_path(instance, id):
    """
    Rename the uploaded video file, generate a thumbnail, 
    and create HLS streams at multiple resolutions.

    Args:
        instance (Video): The Video model instance.
        id (int): The ID of the Video instance.

    Behavior:
        - Renames the original video file to a standardized format.
        - Creates a thumbnail from the video.
        - Converts the video into HLS segments for each target resolution.
    """
    old_path = instance.video_file.path 
    new_name = f"new_video_name_{id}.mp4"
    old = os.path.dirname(old_path)
    new_path = os.path.join(old, new_name)
    os.rename(old_path, new_path)
    get_length(new_path)
    convert_Video_to_thumbnail(new_path,instance)

    for  height, res in resolutions:
        
        convert_Video(id, new_path, res, height)



def get_length(filename):
    """
    Gibt die Dauer einer Videodatei in Sekunden zurück.
    """
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            filename
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    
    # Bytes → String → Whitespace entfernen → Float
    duration = float(result.stdout.decode('utf-8').strip())
    print("Video duration (seconds):", duration)
    print('sehr gut')
    return duration
    



def convert_Video(id, new_path, res, height):
    """
    Convert a video to HLS format at a given resolution.

    Args:
        id (int): Video instance ID.
        new_path (str): Path to the source video.
        res (str): Resolution folder name (e.g., '720p').
        height (str): Target video height (e.g., '720').

    Returns:
        str | None: Path to the generated HLS playlist if successful, else None.
    """
    target_dir = os.path.join('media', 'video', res, str(id))
    os.makedirs(target_dir, exist_ok=True)
    playlist_path = os.path.join(target_dir, "index.m3u8")
    segment_path = os.path.join(target_dir, "segment_%03d.ts")

    ffmpeg_command = [
        '-i', new_path,
        '-vf', f'scale=-2:{height}', 
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-f', 'hls',
        '-hls_time', '6',
        '-hls_playlist_type', 'vod',
       '-hls_base_url', f"/media/video/{res}/{id}/",
        '-hls_segment_filename', segment_path,
        playlist_path
    ]
    if ffmpeg(*ffmpeg_command):
        print('erfolg')
        return playlist_path

    else:
        return None
    
def convert_Video_to_thumbnail(new_path,instance):
    """
    Generate a thumbnail image for a video at 2 seconds into the video.

    Args:
        new_path (str): Path to the source video.
        instance (Video): Video model instance to update with thumbnail.

    Returns:
        str: Path to the generated thumbnail image.
    """

    target_path = os.path.join('media', 'thumbnails', str(instance.id))
    os.makedirs(target_path, exist_ok=True)
    thumbnail_name = f"thumb_{instance.id}.jpg"
    thumbnail_path = os.path.join(target_path, thumbnail_name)

    command  = [
    'ffmpeg',
    '-i',
     new_path,
     '-ss', '00:00:02', 
     '-vframes', '1',
     thumbnail_path]
    
    subprocess.call(command )
    instance.thumbnail_url.name = f"thumbnails/{instance.id}/{thumbnail_name}"
    instance.save(update_fields=['thumbnail_url'])
    return thumbnail_path
    


def ffmpeg(*cmd):
    """
    Helper function to execute an ffmpeg command via subprocess.

    Args:
        *cmd: Variable list of ffmpeg command arguments.

    Returns:
        bool: True if ffmpeg ran successfully, False if an error occurred.
    """
    try:
        subprocess.run(['ffmpeg'] + list(cmd), check=True)
    except subprocess.CalledProcessError:
        return False
    return True