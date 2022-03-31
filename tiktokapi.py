import requests
import json
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()

def get_tiktok_trending():
	url = "https://tiktok-video-no-watermark2.p.rapidapi.com/feed/list"
	api_host = os.environ.get("api-host")
	api_key = os.environ.get("api-key")
	querystring = {"region":"VN","count":"10"}

	headers = {
		"X-RapidAPI-Host": api_host,
		"X-RapidAPI-Key": api_key
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	res = json.loads(response.text)
	data = res['data']
	result = []

	for video in data:
		result.append(
			{
				'title': video['title'],
				'cover': video['origin_cover'],
				'play': video['play'],
				'likes': video['digg_count'],
				'views': video['play_count'],
				'comments': video['comment_count'],
				'shares': video['share_count'],
				'downloads': video['download_count'],
				'author': video['author']['nickname'],
				'author_id': video['author']['unique_id'],
				'author_avatar': video['author']['avatar']
			}
		)
	return result
	print(json.dumps(result, ensure_ascii=False))


get_tiktok_trending()