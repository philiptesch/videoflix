from rest_framework import serializers
from video_app.models import Video


class VideoListSeralizers(serializers.ModelSerializer):

     id = serializers.IntegerField(read_only=True)

     class Meta:
        model = Video
        fields = ['id', 'created_at', 'title', 'description', 'thumbnail_url', 'category']