from tiktokapi import get_tiktok_trending, get_tiktok_trending_by_hashtag


def get_trending(platform):
	if platform == "tiktok":
		get_tiktok_trending()
	else:
		print("Not implement")
  
def get_trending_by_hashtag(platform, hashtag):
    if platform == "tiktok":
        get_tiktok_trending_by_hashtag(hashtag) 
    else:
        print("Not implement")