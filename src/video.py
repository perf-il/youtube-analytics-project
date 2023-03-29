# from channel import Channel
import os
from googleapiclient.discovery import build


class Video:
    """Класс для представления видео"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, video_id):
        self.video_id = video_id
        self.video_response = Video.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=video_id).execute()
        self.title = self.video_response['items'][0]['snippet']['title']
        self.url = 'https://youtu.be/' + self.video_id
        self.view_count = self.video_response['items'][0]['statistics']['viewCount']
        self.like_count = self.video_response['items'][0]['statistics']['likeCount']
        self.duration = self.video_response['items'][0]['contentDetails']['duration']

    def __str__(self):
        return self.title


class PLVideo(Video):
    """Класс для представления плейлиста"""
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def get_playlist(self):
        return Video.youtube.playlistItems().list(playlistId=self.playlist_id, part='contentDetails', maxResults=50,).execute()


