from tiktok_api import get_tiktok_trending, get_tiktok_trending_by_hashtag
from youtube_api import get_youtube_trending, get_youtube_trending_by_hashtag


def get_trending(platform):
    if platform == "tiktok":
        return get_tiktok_trending()
    else:
        youtubeData = get_youtube_trending()
        
        return convert_to_messages(platform ,youtubeData)
  
def get_trending_by_hashtag(platform, hashtag):
    if platform == "tiktok":
        return get_tiktok_trending_by_hashtag(hashtag) 
    else:
        return get_youtube_trending_by_hashtag(hashtag)
    
def convert_to_messages(platform, results):
    datas =[]
    
    if platform == "tiktok":
        print("Not implement")
    else:
        for result in results:
            data = {
                "title" : result["features"][0],
                "image" : result["thumbnail_link"]
            }
            
            datas.append(data)
    return datas