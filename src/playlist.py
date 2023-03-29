import os
import isodate
import datetime

from googleapiclient.discovery import build

from src.video import Video


class PlayList:
    """Класс для представления плейлиста"""
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist_videos = PlayList.youtube.playlistItems().list(playlistId=self.playlist_id,
                                               part='contentDetails, snippet',
                                               maxResults=50,
                                               ).execute()
        self.title = self.playlist_videos['items'][0]['snippet']['title'].split('/')[1].strip()
        self.url = 'https://www.youtube.com/playlist?list=' + self.playlist_videos['items'][0]['snippet']['playlistId']

    @property
    def total_duration(self):
        total_duration = datetime.timedelta()
        for item in self.playlist_videos['items']:
            video = Video(item['snippet']['resourceId']['videoId'])
            video_duration = isodate.parse_duration(video.duration)
            total_duration += video_duration
        return total_duration

    def show_best_video(self):
        max_like = 0
        for item in self.playlist_videos['items']:
            video = Video(item['snippet']['resourceId']['videoId'])
            if int(video.like_count) > max_like:
                best_video = video.url
        return best_video

pl = PlayList('PLguYHBi01DWr4bRWc4uaguASmo7lW4GCb')
#print(pl.show_best_video())

a = "https://youtu.be/9Bv2zltQKQA"
b = pl.show_best_video()
print(a)
print(b)

print(a == b)


