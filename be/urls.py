from be.views import get_channel_stats
from django.urls import path

urlpatterns = [
    path('get-channel-stats', get_channel_stats)
]
