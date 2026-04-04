import subprocess
import os
from pymediainfo import MediaInfo

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
        - Avoids overwriting existing thumbnails
        - Calculate the video's half-duration (used for thumbnail timestamp)
        - Converts the video into HLS segments for each target resolution.
    """
    old_path = instance.video_file.path 
    new_name = f"new_video_name_{id}.mp4"
    old = os.path.dirname(old_path)
    new_path = os.path.join(old, new_name)
    os.rename(old_path, new_path)
 #   video_length = get_length(new_path)
 #   if not instance.thumbnail_url: 
 #       convert_Video_to_thumbnail(new_path,instance, video_length)

    for  height, res in resolutions:
        
        convert_Video(id, new_path, res, height)



#def get_length(filename):
    """
    Reads the video file's metadata to calculate half the duration,
    then converts it to hh:mm:ss format for FFmpeg.

    Args:
        filename (str): Path to the video file

    Returns:
        str: Half of the video's duration in hh:mm:ss format
    """
 #   media_info = MediaInfo.parse(filename)
    
  #  for track in media_info.tracks:
     #   if track.track_type == "Video":
      #      duration = track.duration
        #    half_duration_ms = duration / 2
       #     total_seconds = int(half_duration_ms / 1000)
        #    hours = total_seconds // 3600
        #    minutes = (total_seconds % 3600) // 60
         #   seconds = total_seconds % 60 
         #   print("Duration:", duration, "Duration:",  seconds, "Duration:", total_seconds, "Duration:", hours, "Duration:", minutes  )
         #   return  f"{hours:02d}:{minutes:02d}:{seconds:02d}"

   # return None
    



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
        "-y",
        '-i', new_path,
        "-vf", f"scale=-2:{height}",
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
    
def convert_Video_to_thumbnail(new_path,instance, video_length):
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
     '-ss', video_length,
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