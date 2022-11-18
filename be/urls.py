from be.views import get_channels_stats, get_video_ids, get_channel_detail, get_video_details, get_comments, \
    get_subscriber, get_single_channel, get_channel_photo
from django.urls import path

urlpatterns = [
    path('get-channels-stats', get_channels_stats),
    path('get-channel-detail', get_channel_detail),
    path('get-video-ids', get_video_ids),
    path('get-video-details', get_video_details),
    path('get-comments', get_comments),
    path('get-subscriber', get_subscriber),
    path('get-single-channel', get_single_channel),
    path('get-channel-photo', get_channel_photo)
]
