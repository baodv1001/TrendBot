import sys
import random
import json
import requests

sys.path.insert(0, '../')

from typing import Any, Text, Dict, List
from trending_api import get_trending, get_trending_by_category, get_trending_by_hashtag 
from tiktok_api import get_tiktok_list_trend_by_category, get_tiktok_trending

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet

fb_access_token = "EAAHZBdBZB3kisBABrMf6TlcWGM0ZBLjMhZBM99LrUVhyavHkeiiQJpmykRvWXQre16o6pJsUTf1nzyfpW3QsM77iqYQH9FdNwgrqMCqsC29CxZA4HTZCH2UIuGlbAB0xSByUwVZBdst05ZCc7B1xGUy5cqZBJSVYcvbbGU5IgzTZByFyuLp8Qr9J5S"

class GetName(Action):
    def name(self):
        return 'action_name'
    
    def run(self, dispatcher, tracker, domain):
        
        most_recent_state = tracker.current_state()
        
        sender_id = most_recent_state['sender_id']
        
        r = requests.get('https://graph.facebook.com/{}?fields=first_name,last_name,profile_pic&access_token={}'.format(sender_id, fb_access_token)).json()
        
        first_name = r['first_name']
        last_name = r['last_name']
        
        print("Hello", first_name, ' ', last_name)
        
        return [SlotSet('name', first_name), SlotSet('surname', last_name)]


class ActionTopTrendingTikTok(Action):

    def name(self) -> Text:
        return "action_top_trending_tiktok"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        platform = next(tracker.get_latest_entity_values("platform"),None)
        print("Platform is", platform)

        results = get_tiktok_trending()
        buttons = []
        buttons.append(
                {"title": 'Từ khóa (hashtag)', "payload": '/ask_for_trending_tiktok_by_category{"tiktok_category":"hashtag"}'})
        buttons.append(
                {"title": 'Hiệu ứng (effect)', "payload": '/ask_for_trending_tiktok_by_category{"tiktok_category":"effect"}'})
        buttons.append(
                {"title": 'Âm nhạc (music)', "payload": '/ask_for_trending_tiktok_by_category{"tiktok_category":"music"}'})

        for category in results:
            dispatcher.utter_message(text='{0}: {1} - {2}'.format(category['desc'], category['name'], category['url']))
        
        dispatcher.utter_button_message('Hãy chọn một trong ba loại trend sau:', buttons)
            
        return []

class ActionTopTrendingYoutube(Action):
    
    def name(self) -> Text:
        return "action_top_trending_youtube"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        most_recent_state = tracker.current_state()
        sender_id = most_recent_state['sender_id']
        
        results = get_trending()

        for result in results:    
                dispatcher.utter_message(text='{0} - {1}'.format(result['title'], result['image']))

        return []

class ActionTrendingByHashTag(Action):

    def name(self) -> Text:
        return "action_trending_by_hashtag"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        platform = tracker.get_slot("platform");
        hashtag = tracker.get_slot("hashtag");


        print("Platform is", platform)
        print("Hashtag is", hashtag)
        
        result = get_trending_by_hashtag(platform, hashtag)
        
        for video in result:
            dispatcher.utter_message(text=video['title'], image=video['cover'])

        return []
    

class ActionSelectPlatform(Action):

    def name(self) -> Text:
        return "action_select_platform"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        platform = next(tracker.get_latest_entity_values("platform"),None)
        
        print("Platform is", platform)
        dispatcher.utter_message(text='{0}'.format(platform))

        return []

class ActionTrendingByTikTokCategory(Action):

    def name(self) -> Text:
        return "action_top_tiktok_trending_by_category"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        tiktok_category = next(tracker.get_latest_entity_values("tiktok_category"),None)
        print("Tiktok Category is", tiktok_category)
        
        if tiktok_category:
            dispatcher.utter_message(text='Những trend mới nhất theo {0} là :'.format(tiktok_category))
            results = get_tiktok_list_trend_by_category(tiktok_category)
            for result in results:    
                dispatcher.utter_message(text='{0} - {1}'.format(result['desc'], result['url']))
                dispatcher.utter_attachment(result['videos'][0]['url'])
        else:
            dispatcher.utter_message(text="Em chưa hiểu thể loại anh/chị muốn chọn, vui lòng chọn lại ạ!")
            
        return []

class ActionTrendingByYoutubeCategory(Action):

    def name(self) -> Text:
        return "action_top_youtube_trending_by_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        youtube_category = next(tracker.get_latest_entity_values("youtube_category"),None)
        print("Youtube Category is", youtube_category)
        
        results = get_trending_by_category(youtube_category)

        for result in results:    
            dispatcher.utter_message(text='{0} - {1}'.format(result['title'], result['image']))
            
        return []