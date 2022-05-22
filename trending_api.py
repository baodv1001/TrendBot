from tiktok_api import get_tiktok_trending, get_tiktok_trending_by_hashtag
from youtube_api import get_youtube_trending_by_hashtag


def get_trending(platform):
	if platform == "tiktok":
		return get_tiktok_trending()
	else:
		print("Not implement")
  
def get_trending_by_hashtag(platform, hashtag):
    if platform == "tiktok":
        return get_tiktok_trending_by_hashtag(hashtag) 
    else:
        return get_youtube_trending_by_hashtag(hashtag)