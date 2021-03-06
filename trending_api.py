from tiktok_api import get_tiktok_trending_by_hashtag
from youtube_api import get_more_trending, get_youtube_trending, get_youtube_trending_by_hashtag


def get_trending(userId = '1'):
    youtubeData = get_youtube_trending(userId)
        
    return convert_to_messages(youtubeData)
  
def get_trending_by_hashtag(platform, hashtag, userId = '1'):
    if platform == "tiktok":
        return get_tiktok_trending_by_hashtag(hashtag) 
    else:
        youtubeData = get_youtube_trending_by_hashtag(userId, hashtag)
        
        return convert_to_messages(youtubeData)
    
def get_trending_by_category (category, userId = '1'):
    youtubeData = get_youtube_trending(userId, category)
    
    return convert_to_messages(youtubeData)

def get_more_youtube_trending(userId):
    return convert_to_messages(get_more_trending(userId))
    
def convert_to_messages(results, platform = 'youtube'):
    datas =[]
    
    if platform == "youtube":   
        for result in results:
            data = {
                "title" : result["features"][0],
                "image" : result["thumbnail_link"],
                "id" : result["id"]
            }
            
            datas.append(data)
            
    return datas