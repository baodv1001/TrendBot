import os, requests, sys, time, json
from unicodedata import category

import googleapiclient.discovery

COUNTRY_CODE = "VN"
API_KEY = ""

api_service_name = "youtube"
api_version = "v3"

snippet_features = ["title", "channelTitle"]

def get_youtube_api_config():
    return os.environ.get("youtube-api-key")

def api_request(categoryId = None):
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = API_KEY)
    
    request = youtube.videos().list(
        part = "snippet,contentDetails,statistics",
        chart = "mostPopular",
        maxResults = 3,
        regionCode = COUNTRY_CODE,
        videoCategoryId = categoryId
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


def get_youtube_trending(categoryName = None):  
    categoryId = get_category_Id(categoryName)

    video_data_page = api_request(categoryId)
    
    items = video_data_page.get("items", [])
    
    data = get_videos(items)
    
    return data

def get_youtube_trending_by_hashtag(hashtag):
    print ('Implementing: ' + hashtag)

def get_category_Id (categoryName):
    switcher = {
            'film' : 1,
            'animation' : 1,
            'autos' : 2,
            'vehicles' : 2,
            'music' : 10,
            'pets' : 15,
            'animals' : 15,
            'sports' : 17,
            'travel' : 19,
            'events' : 19,
            'gaming' : 20,
            'people ' : 22,
            'blogs' : 22,
            'comedy' : 23,
            'entertainment' : 24,
            'news' : 25,
            'politics' : 25,
            'howto' : 26,
            'style' : 26,
            'education' : 27,
            'science' : 28,
            'technology' : 28,
    }
    
    return switcher.get(categoryName,None)

print(get_youtube_trending('music'))