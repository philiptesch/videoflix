from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .seralizers import VideoListSeralizers
from video_app.models import Video
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
import os
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from pathlib import Path
from django.http import HttpResponse
from django.http import FileResponse, Http404

class ListVideoView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VideoListSeralizers
    queryset = Video.objects.all()


class VideoResolutionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):

        movie_id = self.kwargs.get('movie_id')
        resolution = self.kwargs.get('resolution')

        video_exists = Video.objects.filter(pk=movie_id).exists()
        if not video_exists:
            return Response({"detail": "Video not found"}, status=status.HTTP_404_NOT_FOUND)

        path = Path(settings.MEDIA_ROOT)  / 'video' / resolution / str(movie_id) / 'index.m3u8'


        if not os.path.exists(path):
            return Response({"detail": "Playlist not found"},status=status.HTTP_404_NOT_FOUND)

        with open(path, 'r', encoding="utf-8") as file:
            manifest_content = file.read()

        return HttpResponse(
            content=manifest_content, 
            content_type='application/vnd.apple.mpegurl'
        )


class VideoSegmentView(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request, *args, **kwargs):

        movie_id = self.kwargs.get('movie_id')
        resolution = self.kwargs.get('resolution')
        segment = self.kwargs.get('segment')

        segment_file = os.path.basename(segment)

        video_exists = Video.objects.filter(pk=movie_id).exists()
        if not video_exists:
            return Response({"detail": "Video not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if not segment_file.endswith(".ts"):
            return Response({"detail": "Invalid segment type"}, status=400)
        
        path = Path(settings.MEDIA_ROOT) / 'video' / resolution / str(movie_id) / str(segment)
                
        if os.path.exists(path):
            return FileResponse(open(path, 'rb'), content_type='video/MP2T')
        raise Http404("Segment not found")







