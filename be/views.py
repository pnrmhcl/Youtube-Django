import pandas as pd
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from googleapiclient.discovery import build

from YoutubeApi.responses import response_200

api_key = 'AIzaSyDEtBuQVc_M71w5odpUzKC2TAnGZGoDF3A'
channel_ids = ['UCtXgBWNjyHrH2e-IbtIqDdQ']
playlist_id = 'PLEGyvPj66Tepi7iGf5NNVilCHnWyZabzq'
youtube = build('youtube', 'v3', developerKey=api_key)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_channel_stats(request):
    all_data = []
    request = youtube.channels().list(
        part='snippet,contentDetails,statistics', id=','.join(channel_ids))
    response = request.execute()
    for i in range(len(response['items'])):
        data = dict(Channel_name=response['items'][i]['snippet']['title'],
                    Subscribers=response['items'][i]['statistics']['subscriberCount'],
                    Views=response['items'][i]['statistics']['viewCount'],
                    Total_videos=response['items'][i]['statistics']['viewCount'])
        all_data.append(data)
    return response_200(data=all_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_channel_detail(request):
    all_data = []
    request = youtube.channels().list(
        part='snippet,contentDetails,statistics', id=','.join(channel_ids))
    response = request.execute()
    for i in range(len(response['items'])):
        data = dict(Channel_name=response['items'][i]['snippet']['title'],
                    Subscribers=response['items'][i]['statistics']['subscriberCount'],
                    Views=response['items'][i]['statistics']['viewCount'],
                    Total_videos=response['items'][i]['statistics']['viewCount'],
                    playlist_id=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_data.append(data)
    return response_200(data=all_data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_video_ids(request):
    request = youtube.playlistItems().list(part='contentDetails',
                                           playlistId=playlist_id)
    response = request.execute()
    return response_200(data=response)
