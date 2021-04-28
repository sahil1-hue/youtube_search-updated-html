from django.shortcuts import render
import requests
from django.conf import settings


# Create your views here.
def searchYT(request):
    Video_Information_list = []
    if request.method == 'POST':
        YOUTUBE_DATA_API_KEY = 'AIzaSyCW3FJHM-EhyCPK1DVJNwLd4AY7tsJTFcY'
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'
        for_search = {
            'part': 'snippet',
            'q': request.POST['search'],
            'key': YOUTUBE_DATA_API_KEY,
            'type': 'video',
             'maxResults': 5

        }
        vid_ids = []
        request_for_search = requests.get(search_url, params=for_search)

        results = request_for_search.json()['items']
        for result in results:

            vid_ids.append(result['id']['videoId'])

        for_video = {
            'part': 'snippet',
            'key': YOUTUBE_DATA_API_KEY,
            'id': ','.join(vid_ids)

        }

        request_for_videos = requests.get(video_url, params=for_video)
        results = request_for_videos.json()['items']
        for result in results:
            InformationAboutVideo = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'thumbnail': result['snippet']['thumbnails']['high']['url'],
                'url': f'https://www.youtube.com/watch?v={result["id"]}'

            }
            Video_Information_list.append(InformationAboutVideo)
    context = {

        'videoInformationList': Video_Information_list

    }

    return render(request, 'youtube_search/index.html', context)
