from django.urls import path
from .views import ListVideoView, VideoResolutionView, VideoSegmentView

urlpatterns = [
   path('video/', ListVideoView.as_view(), name='video_List'),
   path('video/<int:movie_id>/<str:resolution>/index.m3u8', VideoResolutionView.as_view(), name='video_Resolution_List'),
    path('video/<int:movie_id>/<str:resolution>/<str:segment>/', VideoSegmentView.as_view(), name='video_Segment_List'),
]