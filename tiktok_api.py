import requests
import json
import numpy as np
from dotenv import load_dotenv
import os
import random
from sqlalchemy import null

load_dotenv()
api_host_1 = os.environ.get("api-host-1")
api_key = os.environ.get("api-key")
api_host_2 = os.environ.get("api-host-2")

def convert_category(categories):
	result = []

	for category in categories:
		# hashtag
		if(category['category_type'] == 0):
			result.append(
				{
					'desc': category['desc'],
					'type': category['category_type'],
					'name': category['challenge_info']['cha_name'],
					'id': category['challenge_info']['cid'],
					'user_count': category['challenge_info']['user_count'],
					'view_count': category['challenge_info']['view_count'],
					'author': '',
					'url': 'https://www.tiktok.com/tag/{0}'.format(category['challenge_info']['cha_name'])
				}
			)
   
		# effect
		if(category['category_type'] == 3):
			result.append(
				{
					'desc': category['desc'],
					'type': category['category_type'],
					'name': category['effect_info']['name'],
					'id': category['effect_info']['effect_id'],
					'user_count': category['effect_info']['user_count'],
					'view_count': category['effect_info']['vv_count'],
					'author': category['effect_info']['owner_nickname'],
					'url': 'https://www.tiktok.com/sticker/{0}-{1}'.format(category['effect_info']['name'].replace(' ','-'),category['effect_info']['effect_id'] )
				}
			)
   
		# music
		if(category['category_type'] == 1):
			result.append(
				{
					'desc': category['desc'],
					'type': category['category_type'],
					'name': category['music_info']['title'],
					'id': category['music_info']['mid'],
					'user_count': category['music_info']['user_count'],
					'view_count': 0,
					'author': category['music_info']['author'],
					'url': 'https://www.tiktok.com/music/{0}-{1}'.format(category['music_info']['title'].replace(' ','-'), category['music_info']['mid'])
				}
			)

	return result

def get_tiktok_trending():
	url = "https://tokapi-mobile-version.p.rapidapi.com/v1/category"

	querystring = {"count":"20","region":"VN"}

	headers = {
		"X-RapidAPI-Host": api_host_2,
		"X-RapidAPI-Key": api_key
	}

	response = requests.request("GET", url, headers=headers, params=querystring)

	res = json.loads(response.text)

	categories = res['category_list']

	res = convert_category(categories)

	jsonFile = open("data/data.json", "w")
	jsonFile.write(json.dumps(res))
	jsonFile.close()

	return res

def get_tiktok_list_trend_by_category(category):
	f = open('data/data.json')
	data = json.load(f)
	
	type = null;

	if category == 'hashtag':
		type = 0
	if category == 'music':
		type = 1
	if category == 'effect':
		type = 3		

	res = []
	for category in data:
		if category['type'] == type:
			videos = get_video_by_category(category)
			if len(videos) > 0:
				category["videos"] = videos
				res.append(category)
	return res

def get_tiktok_trending_by_hashtag(hashtag):
	url = "https://tiktok-video-no-watermark2.p.rapidapi.com/challenge/search"
 
	querystring = {"keywords": hashtag, "count": "3", "region": "VN"}

	headers = {
		"X-RapidAPI-Host": api_host_1,
		"X-RapidAPI-Key": api_key
	}

	response = requests.request("GET", url, headers=headers, params=querystring)

	res = json.loads(response.text)
 
	data = res['data']['challenge_list']
 
	challenge = data[0]
 
	videos = get_hashtag_video_by_id(challenge['id'])
 
	# videos = res_data['videos']
	
	return convert_data(videos)

def get_hashtag_video_by_id(id):

	url = "https://tiktok-video-no-watermark2.p.rapidapi.com/challenge/posts"

	querystring = {"challenge_id":id}

	headers = {
		"X-RapidAPI-Host": api_host_1,
		"X-RapidAPI-Key": api_key
	}
 
	response = requests.request("GET", url, headers=headers, params=querystring)
 
	res = json.loads(response.text)
 
	data = res['data']

	jsonFile = open("data/hashtag.json", "w")
	jsonFile.write(json.dumps(res))
	jsonFile.close()
 
	return random.choices(data['videos'], k=3);

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

def get_video_by_category(category):
	if category['type']==0:
		return get_video_by_challenge(category['id'])
	elif category['type']==1:
		return get_video_by_music(category['id'])
	elif category['type']==3:
		return get_video_by_effect(category['id'])
	

def get_video_by_music(id):
	url = 'https://tokapi-mobile-version.p.rapidapi.com/v1/music/posts/{0}'.format(id)

	querystring = {"count":"1"}

	headers = {
		"X-RapidAPI-Host": api_host_2,
		"X-RapidAPI-Key": api_key
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	res = json.loads(response.text)
	if "aweme_list" in res:
		videos = convert_video_from_aweme(res['aweme_list'])
	else:
		videos = []
	return videos

def get_video_by_challenge(id):
	url = "https://tokapi-mobile-version.p.rapidapi.com/v1/hashtag/posts/{0}".format(id)

	querystring = {"count":"1"}

	headers = {
		"X-RapidAPI-Host": api_host_2,
		"X-RapidAPI-Key": api_key
	}

	response = requests.request("GET", url, headers=headers, params=querystring)

	res = json.loads(response.text)
	
	
	if "aweme_list" in res:
		videos = convert_video_from_aweme(res['aweme_list'])
	else:
		videos = []
	return videos

def get_video_by_effect(id):
	url = "https://tokapi-mobile-version.p.rapidapi.com/v1/sticker/posts/{0}".format(id)

	querystring = {"count":"1"}

	headers = {
		"X-RapidAPI-Host": api_host_2,
		"X-RapidAPI-Key": api_key
	}

	response = requests.request("GET", url, headers=headers, params=querystring)

	res = json.loads(response.text)
	if "aweme_list" in res:
		videos = convert_video_from_aweme(res['aweme_list'])
	else:
		videos = []
	
	return videos

def convert_video_from_aweme(awemes):
	result = []

	for aweme in awemes:
		result.append({
			'title': aweme['desc'],
			'cover': aweme['video']['cover']['url_list'][0],
			'url': aweme['share_url'],
			'likes': aweme['statistics']['digg_count'],
			'views': aweme['statistics']['play_count'],
			'comments': aweme['statistics']['comment_count'],
			'shares': aweme['statistics']['share_count'],
			'downloads': aweme['statistics']['download_count'],
			'author': aweme['author']['nickname'],
			'author_id': aweme['author']['unique_id'],
			'author_avatar': aweme['author']['avatar_larger']['url_list'][0]
		})

	return result
