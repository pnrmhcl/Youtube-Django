from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from googleapiclient.discovery import build
from YoutubeApi.responses import response_200


@api_view(['POST'])
@permission_classes([AllowAny])
def get_channels_stats(request):
    api_key = request.data['apiKey']
    youtube = build('youtube', 'v3', developerKey=api_key)
    channel_id = request.data['channelId']
    all_data = []
    request = youtube.channels().list(part='snippet,contentDetails,statistics', id=channel_id)
    response = request.execute()
    for i in range(len(response['items'])):
        data = dict(
            channelName=response['items'][i]['snippet']['title'],
            viewCount=response['items'][i]['statistics']["viewCount"],
            subscriberCount=response['items'][i]['statistics']["subscriberCount"],
            videoCount=response['items'][i]['statistics']["videoCount"])
        all_data.append(data)
    return response_200(data=all_data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_single_channel(request):
    api_key = request.data['apiKey']
    youtube = build('youtube', 'v3', developerKey=api_key)
    channel_id = request.data['channelId']
    request = youtube.channels().list(part='snippet,contentDetails,statistics', id=channel_id)
    response = request.execute()
    data = dict(
        channelName=response['items'][0]['snippet']['title'],
        viewCount=response['items'][0]['statistics']['viewCount'],
        subscriberCount=response['items'][0]['statistics']['subscriberCount'],
        videoCount=response['items'][0]['statistics']['videoCount'])
    return response_200(data=data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_channel_detail(request):
    api_key = request.data['apiKey']
    youtube = build('youtube', 'v3', developerKey=api_key)
    channel_id = request.data['channelId']
    request = youtube.channels().list(part='snippet,contentDetails,statistics', id=channel_id)
    response = request.execute()
    data = dict(
        snippet=response['items'][0]['snippet'],
        totalView=response['items'][0]['statistics']['viewCount'],
        totalVideo=response['items'][0]['statistics']['videoCount'],
        subscriberCount=response['items'][0]['statistics']['subscriberCount'])
    return response_200(data=data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_channel_photo(request):
    api_key = request.data['apiKey']
    youtube = build('youtube', 'v3', developerKey=api_key)
    channel_id = request.data['channelId']
    request = youtube.channels().list(part='snippet,contentDetails,statistics', id=channel_id)
    response = request.execute()
    data = dict(response['items'][0]["snippet"]["thumbnails"])
    return response_200(data=data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_playlist_video_id(request):
    api_key = request.data['apiKey']
    youtube = build('youtube', 'v3', developerKey=api_key)
    playlist_id = request.data['playlistId']
    request = youtube.playlistItems().list(part='contentDetails', playlistId=playlist_id)
    response = request.execute()
    video_ids = []
    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails'])
    next_page_token = response.get('nextPageToken')
    more_pages = True
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(part='contentDetails', playlistId=playlist_id,
                                                   pageToken=next_page_token)
            response = request.execute()
            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails'])
            next_page_token = response.get('nextPageToken')
    return response_200(data=video_ids)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_video_details(request):
    api_key = request.data['apiKey']
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_ids = request.data['videoId']
    all_video_stats = []
    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(part='snippet,statistics', id=','.join(video_ids[i:i + 50]))
        response = request.execute()
        for video in response['items']:
            video_stats = {}
            video_stats["statistics"] = video['statistics']
            video_stats["snippet"] = video['snippet']
            all_video_stats.append(video_stats)
    return response_200(data=all_video_stats)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_video_comments(request):
    api_key = request.data['apiKey']
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_id = request.data['videoId']
    all_data = []
    request1 = youtube.commentThreads().list(part="snippet", videoId=video_id, maxResults=100).execute()
    while True:
        data = request2 = youtube.commentThreads().list(part="snippet", videoId=video_id, maxResults=100,
                                                        textFormat="plainText").execute()
        for item in data["items"]:
            comment = item["snippet"]["topLevelComment"]
            comment_data = dict(
                comment=item["snippet"]["topLevelComment"],
                author=comment["snippet"]["authorDisplayName"],
                text=comment["snippet"]["textDisplay"])
            all_data.append(comment_data)
        return response_200(data=all_data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_subscriber(request):
    api_key = request.data['apiKey']
    channel_id = request.data['channelId']
    youtube = build('youtube', 'v3', developerKey=api_key)
    all_data = []
    request = youtube.subscriptions().list(part="snippet", channelId=channel_id)
    response = request.execute()
    for item in response["items"]:
        comment_data = item["snippet"]
        all_data.append(comment_data)
    return response_200(data=all_data)


@api_view(['POST'])
@permission_classes([AllowAny])
def video_category(request):
    api_key = request.data['apiKey']
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videoCategories().list(part='snippet', regionCode='IN')
    response = request.execute()
    return response_200(data=response)
