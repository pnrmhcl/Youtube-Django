import pandas as pd
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from googleapiclient.discovery import build

from YoutubeApi.responses import response_200

api_key = 'AIzaSyDEtBuQVc_M71w5odpUzKC2TAnGZGoDF3A'
channel_ids = ['UCtXgBWNjyHrH2e-IbtIqDdQ']
playlist_id = 'PLEGyvPj66Tepi7iGf5NNVilCHnWyZabzq'
video_ids = ["z4Cxn1lDPXo", "NeSpx7vZifc", "khq8q5V3vzM"]
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
                                           playlistId=playlist_id,
                                           maxResults=50
                                           )
    response = request.execute()
    video_ids = []
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])
    next_page_token = response.get('nextPageToken')
    more_pages = True
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(part='contentDetails',
                                                   playlistId=playlist_id,
                                                   maxResults=50,
                                                   pageToken=next_page_token)
            response = request.execute()
            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])
            next_page_token = response.get('nextPageToken')

    return response_200(data=video_ids)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_video_details(request):
    all_video_stats = []
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(video_ids[i:i + 50]))

        response = request.execute()

        for video in response['items']:
            video_stats = dict(Title=video['snippet']['title'],
                               Published_date=video['snippet']['publishedAt'],
                               Views=video['statistics']['viewCount'],
                               Likes=video['statistics']['likeCount'],
                               Comments=video['statistics']['commentCount']
                               )
            all_video_stats.append(video_stats)
    return response_200(data=all_video_stats)
