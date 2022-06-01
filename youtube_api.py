import os, requests, sys, time, json

import googleapiclient.discovery

COUNTRY_CODE = "VN"
API_KEY = ""

api_service_name = "youtube"
api_version = "v3"

snippet_features = ["title", "channelTitle"]

def get_youtube_api_config():
    return os.environ.get("youtube-api-key")

def api_request():
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = API_KEY)
    
    request = youtube.videos().list(
        part = "snippet,contentDetails,statistics",
        chart = "mostPopular",
        maxResults = 3,
        regionCode = COUNTRY_CODE
    )
    
    response = request.execute()
    
    return response

def get_videos(items):
    lines = []
    for video in items:
        if "statistics" not in video:
            continue

        video_id = video["id"]
        snippet = video["snippet"]

        features = [(snippet.get(feature, "")) for feature in snippet_features]

        thumbnail_link = (
            snippet.get("thumbnails", dict()).get("medium", dict()).get("url", "")
        )

        line = {
            "id": video_id,
            "features": features,
            "thumbnail_link": (thumbnail_link),
        }
        
        lines.append(line)
    return lines


def get_youtube_trending():    
    video_data_page = api_request()
    
    items = video_data_page.get("items", [])
    
    data = get_videos(items)
    
    return data

def get_youtube_trending_by_hashtag(hashtag):
    return [{'title':'implementing', 'cover':'image-test.png' }]