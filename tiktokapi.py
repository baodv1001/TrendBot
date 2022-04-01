import requests
import json
import numpy as np
from dotenv import load_dotenv
import os

load_dotenv()
api_host = os.environ.get("api-host")
api_key = os.environ.get("api-key")

def get_tiktok_trending():
	url = "https://tiktok-video-no-watermark2.p.rapidapi.com/feed/list"
	querystring = {"region":"VN","count":"10"}

	headers = {
		"X-RapidAPI-Host": api_host,
		"X-RapidAPI-Key": api_key
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	res = json.loads(response.text)
	data = res['data']
	return convert_data(data)
	print(json.dumps(result, ensure_ascii=False))

def get_tiktok_trending_by_hashtag(hashtag):
	url = "https://tiktok-video-no-watermark2.p.rapidapi.com/challenge/search"

	querystring = {"keywords": hashtag}

	headers = {
		"X-RapidAPI-Host": api_host,
		"X-RapidAPI-Key": api_key
	}

	response = requests.request("GET", url, headers=headers, params=querystring)

	res = json.loads(response.text)
	data = res['data']['challenge_list']
	challenge = data[0]
	res_data = get_hashtag_video_by_id(challenge['id'])
	videos = res_data['videos']
	print(convert_data(videos))
	return convert_data(videos)

def get_hashtag_video_by_id(id):

	url = "https://tiktok-video-no-watermark2.p.rapidapi.com/challenge/posts"

	querystring = {"challenge_id":id}

	headers = {
		"X-RapidAPI-Host": api_host,
		"X-RapidAPI-Key": api_key
	}
 
	response = requests.request("GET", url, headers=headers, params=querystring)
	res = json.loads(response.text)
	data = res['data']
	return data;

def convert_data(data):
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

get_tiktok_trending_by_hashtag("cosplay")
