from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .seralizers import VideoListSeralizers
from video_app.models import Video
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
import os
from rest_framework.response import Response
from rest_framework import status

class ListVideoView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VideoListSeralizers
    queryset = Video.objects.all()


class VideoResolutionView(APIView):
    serializer_class = VideoListSeralizers
    
    
    def get(self, request, *args, **kwargs):

        pk = self.kwargs.get('pk')
        resolution = self.kwargs.get('resolution')
        obj = get_object_or_404(Video, pk=pk)
        path = f"media/video/{resolution}/{str(pk)}"

        if not os.path.exists(path):
            return Response({"detail": "Playlist not found"},status=status.HTTP_404_NOT_FOUND)








