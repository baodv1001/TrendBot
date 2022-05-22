import os, requests, sys, time, json

COUNTRY_CODE = "VN"
API_KEY = ""

snippet_features = ["title", "publishedAt", "channelTitle"]

def api_request(page_token, country_code):
    request_url = f"https://www.googleapis.com/youtube/v3/videos?part=id,statistics,snippet{page_token}chart=mostPopular&regionCode={country_code}&maxResults=5&key={API_KEY}"
    
    request = requests.get(request_url)
    
    if request.status_code == 429:
        print("Temp-Banned due to excess requests, please wait and continue later")
        sys.exit()
    
    return request.json()

def get_youtube_api_config():
    return os.environ.get("youtube-api-key")

def get_videos(items):
    lines = []
    for video in items:
        if "statistics" not in video:
            continue

        video_id = video["id"]
        snippet = video["snippet"]

        features = [(snippet.get(feature, "")) for feature in snippet_features]

        thumbnail_link = (
            snippet.get("thumbnails", dict()).get("default", dict()).get("url", "")
        )
        trending_date = time.strftime("%y.%d.%m")

        line = {
            "id": video_id,
            "features": features,
            "trending_date": (trending_date),
            "thumbnail_link": (thumbnail_link),
        }
        lines.append(line)
    return lines


def get_youtube_trending_by_hashtag(hashtag):
    data = []
    next_page_token="&"
    
    global API_KEY
    API_KEY = get_youtube_api_config()
    
    while next_page_token is not None:
        video_data_page = api_request(next_page_token, COUNTRY_CODE)
        
        next_page_token = video_data_page.get("nextPageToken", None)
        
        next_page_token = (
            f"&pageToken={next_page_token}&"
            if next_page_token is not None
            else next_page_token
        )
        
        items = video_data_page.get("items", [])
        data += get_videos(items)
    
    print(data)
    
    return [{'title':'implementing', 'cover':'image-test.png' }]
