from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from googleapiclient.discovery import build

from YoutubeApi.responses import response_200

api_key = 'AIzaSyDEtBuQVc_M71w5odpUzKC2TAnGZGoDF3A'
channel_id = 'UCtXgBWNjyHrH2e-IbtIqDdQ'

youtube = build('youtube', 'v3', developerKey=api_key)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_channel_stats(request):
    request = youtube.channels().list(
        part='snippet,contentDetails,statistics', id=channel_id)
    response = request.execute()
    data = dict(Channel_name=response['items'][0]['snippet']['title'],
                Subscribers=response['items'][0]['statistics']['subscriberCount'],
                Views=response['items'][0]['statistics']['viewCount'],
                Total_videos=response['items'][0]['statistics']['viewCount']

                )
    return response_200(data=data)
