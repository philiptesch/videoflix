from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .seralizers import VideoListSeralizers
from video_app.models import Video


class ListVideoView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = VideoListSeralizers
    queryset = Video.objects.all()