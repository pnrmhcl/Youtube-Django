from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from googleapiclient.discovery import build

from YoutubeApi.exception import is_request_valid
from YoutubeApi.responses import response_200, response_400


@api_view(['POST'])
@permission_classes([AllowAny])
def get_channels_stats(request):
    should_contain_key_values = ["apiKey", "channelId"]
    if not is_request_valid(request.data, should_contain_key_values):
        return response_400()
    api_key = request.data['apiKey']
    channel_id = request.data['channelId']

    youtube = build('youtube', 'v3', developerKey=api_key)
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
    should_contain_key_values = ["apiKey", "channelId"]
    if not is_request_valid(request.data, should_contain_key_values):
        return response_400()
    api_key = request.data['apiKey']
    channel_id = request.data['channelId']

    youtube = build('youtube', 'v3', developerKey=api_key)
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
    should_contain_key_values = ["apiKey", "channelId"]
    if not is_request_valid(request.data, should_contain_key_values):
        return response_400()
    api_key = request.data['apiKey']
    channel_id = request.data['channelId']

    youtube = build('youtube', 'v3', developerKey=api_key)
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
    should_contain_key_values = ["apiKey", "channelId"]
    if not is_request_valid(request.data, should_contain_key_values):
        return response_400()
    api_key = request.data['apiKey']
    channel_id = request.data['channelId']

    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.channels().list(part='snippet,contentDetails,statistics', id=channel_id)
    response = request.execute()
    data = dict(response['items'][0]["snippet"]["thumbnails"])
    return response_200(data=data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_playlist_video_id(request):
    should_contain_key_values = ["apiKey", "playlistId"]
    if not is_request_valid(request.data, should_contain_key_values):
        return response_400()
    api_key = request.data['apiKey']
    playlist_id = request.data['playlistId']

    youtube = build('youtube', 'v3', developerKey=api_key)
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
    should_contain_key_values = ["apiKey", "videoId"]
    if not is_request_valid(request.data, should_contain_key_values):
        return response_400()
    api_key = request.data['apiKey']
    video_ids = request.data['videoId']

    youtube = build('youtube', 'v3', developerKey=api_key)
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
    should_contain_key_values = ["apiKey", "videoId"]
    if not is_request_valid(request.data, should_contain_key_values):
        return response_400()
    api_key = request.data['apiKey']
    video_id = request.data['videoId']

    youtube = build('youtube', 'v3', developerKey=api_key)
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
    should_contain_key_values = ["apiKey", "channelId"]
    if not is_request_valid(request.data, should_contain_key_values):
        return response_400()
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
    should_contain_key_values = ["apiKey"]
    if not is_request_valid(request.data, should_contain_key_values):
        return response_400()
    api_key = request.data['apiKey']

    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videoCategories().list(part='snippet', regionCode='IN')
    response = request.execute()
    return response_200(data=response)


@api_view(['POST'])
@permission_classes([AllowAny])
def most_popular_video_details(request):
    should_contain_key_values = ["apiKey"]
    if not is_request_valid(request.data, should_contain_key_values):
        return response_400()
    api_key = request.data['apiKey']

    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(
        part="id, snippet, contentDetails, statistics",
        chart='mostPopular', regionCode='IN')
    response = request.execute()
    return response_200(data=response)


@api_view(['POST'])
@permission_classes([AllowAny])
def caption_list(request):
    should_contain_key_values = ["apiKey"]
    if not is_request_valid(request.data, should_contain_key_values):
        return response_400()
    api_key = request.data['apiKey']
    video_id = request.data['videoId']

    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.captions().list(
        part="id,snippet", videoId=video_id
    )
    response = request.execute()
    return response_200(data=response)
