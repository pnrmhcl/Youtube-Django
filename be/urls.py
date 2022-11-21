from be.views import get_channels_stats, get_playlist_video_id, get_channel_detail, get_video_details, \
    get_video_comments, get_subscriber, get_single_channel, get_channel_photo, video_category, \
    most_popular_video_details, caption_list
from django.urls import path

urlpatterns = [
    path('get-channels-stats', get_channels_stats),
    path('get-channel-detail', get_channel_detail),
    path('get-playlist-video-id', get_playlist_video_id),
    path('get-video-details', get_video_details),
    path('get-video-comments', get_video_comments),
    path('get-subscriber', get_subscriber),
    path('get-single-channel', get_single_channel),
    path('get-channel-photo', get_channel_photo),
    path('video-category', video_category),
    path('most-popular-video-details', most_popular_video_details),
    path('caption-list', caption_list)
]
