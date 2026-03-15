from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import  status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from .seralizers import VideoListSeralizers
from video_app.models import Video
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class ListVideoView(ListAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = VideoListSeralizers
    queryset = Video.objects.all()
    

