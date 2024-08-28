import requests
from typing import List
from app.core.config import settings
from app.schemas.YouTubeVideo import YouTubeVideo


def search_youtube_videos(query: str) -> List[YouTubeVideo]:
    url = 'https://google.serper.dev/videos'
    headers = {
        'X-API-KEY': settings.SERPER_API_KEY,
        'Content-Type': 'application/json'
    }
    data = {
        "q": query,
        "gl": "bd",
        "num": 4
    }

    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()

    videos = []
    for video in response_data.get('videos', [])[:5]:
        video_data = YouTubeVideo(
            title=video.get('title'),
            link=video.get('link'),
            imageUrl=video.get('imageUrl'),
            duration=video.get('duration'),
            source=video.get('source'),
            date=video.get('date')
        )
        videos.append(video_data)

    return videos
