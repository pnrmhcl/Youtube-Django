from be.views import get_channel_stats, get_video_ids, get_channel_detail
from django.urls import path

urlpatterns = [
    path('get-channel-stats', get_channel_stats),
    path('get-channel-detail', get_channel_detail),
    path('get-video-ids', get_video_ids)
]
