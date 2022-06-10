import os, requests, sys, time, json
from unicodedata import category
from dotenv import load_dotenv
import googleapiclient.discovery

from recommend_service.item import add_new_item
from recommend_service.service import get_youtube_recommend_video
from recommend_service.user import add_new_user, get_user_num
load_dotenv()

COUNTRY_CODE = "VN"

api_service_name = "youtube"
api_version = "v3"

snippet_features = ["title", "channelTitle"]

def get_youtube_api_config():
    return os.environ.get("youtube-api-key")

def api_request(categoryId = None):
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = get_youtube_api_config())
    
    request = youtube.videos().list(
        part = "snippet,contentDetails,statistics",
        chart = "mostPopular",
        maxResults = 20,
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


def get_youtube_trending(userId, categoryName = None):
    categoryId = None
    if categoryName != None:
        categoryId = get_category_Id(categoryName)

    video_data_page = api_request(categoryId)
    
    items = video_data_page.get("items", [])
    
    datas = get_videos(items)
    
    for data in datas:
        add_new_item(data['id'])
    add_new_user(userId)
    
    jsonFile = open("data/data_youtube.json", "w")
    jsonFile.write(json.dumps(datas))
    jsonFile.close()
    
    userNum = get_user_num(userId)
    
    userWatchFilePath = "../recommend_service/user_watch/{0}.dat".format(userNum)
    
    if os.path.exists(userWatchFilePath):
        os.remove(userWatchFilePath)
    
    recommendDatas = get_youtube_recommend_video(userId)
    
    return recommendDatas

def get_more_trending(userId):
    return get_youtube_recommend_video(userId)

def get_youtube_trending_by_hashtag(hashtag):
    print ('Youtube_API - Hashtag: {0}'.format(hashtag))

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
            'science' : 28,
            'technology' : 28,
    }
    
    return switcher.get(categoryName, 1)