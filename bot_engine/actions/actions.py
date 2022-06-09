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
        
        ##Enable when using messeger
        # most_recent_state = tracker.current_state()
        
        # sender_id = most_recent_state['sender_id']
        
        # r = requests.get('https://graph.facebook.com/{}?fields=first_name,last_name,profile_pic&access_token={}'.format(sender_id, fb_access_token)).json()
        
        # first_name = r['first_name'] 
        # last_name = r['last_name'] 
        
        ##Default
        first_name = 'Rasa'
        last_name = 'Shell'
        
        print("GetName_Action - FirstName: {0} - LastName: {1}".format(first_name, last_name))
        
        return [SlotSet('name', first_name), SlotSet('surname', last_name)]


class ActionTopTrendingTikTok(Action):

    def name(self) -> Text:
        return "action_top_trending_tiktok"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("TopTrendingTiktok_Action")

        results = get_tiktok_trending()
        buttons = []
        buttons.append(
                {"title": 'Từ khóa (hashtag)', "payload": '/ask_for_trending_tiktok_by_category{"tiktokCategory":"hashtag"}'})
        buttons.append(
                {"title": 'Hiệu ứng (effect)', "payload": '/ask_for_trending_tiktok_by_category{"tiktokCategory":"effect"}'})
        buttons.append(
                {"title": 'Âm nhạc (music)', "payload": '/ask_for_trending_tiktok_by_category{"tiktokCategory":"music"}'})

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
        
        print("TopTrendingYoutube_Action")
        
        most_recent_state = tracker.current_state()
        
        #implementing
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

        platform = tracker.get_slot("platform")
        hashtag = tracker.get_slot("hashtag")

        print("TrendingByHashTag_Action - Platform: {0} - Hashtag: {1}".format(platform, hashtag))
        
        result = get_trending_by_hashtag(platform, hashtag)
        
        for video in result:
            dispatcher.utter_message(text=video['title'], attachment=video['play'])

        return []

class ActionTrendingByTikTokCategory(Action):

    def name(self) -> Text:
        return "action_top_tiktok_trending_by_category"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        tiktokCategory = next(tracker.get_latest_entity_values("tiktokCategory"),None)
        
        print("TrendingByTiktokCategory_Action - Category: {0}".format(tiktokCategory))
        
        if tiktokCategory:
            dispatcher.utter_message(text='Những trend mới nhất trên tiktok theo {0} là :'.format(tiktokCategory))
            results = get_tiktok_list_trend_by_category(tiktokCategory)
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
        
        youtubeCategory = next(tracker.get_latest_entity_values("youtubeCategory"),None)
        
        print("TrendingByYoutubeCategory_Action - Category: {0}".format(youtubeCategory))
        
        results = get_trending_by_category(youtubeCategory)

        for result in results:    
            dispatcher.utter_message(text='{0} - {1}'.format(result['title'], result['image']))
            
        return [SlotSet('youtubeCategory', youtubeCategory), SlotSet('platform', 'youtube')]
    
class ActionSeeMore(Action):
    
    def name(self) -> Text:
        return "action_see_more_trending"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        platform = tracker.get_slot("platform")
        hashtag = tracker.get_slot("hashtag")
        youtubeCategory = tracker.get_slot("youtubeCategory")
        tiktokCategory = tracker.get_slot("tiktokCategory")
        
        print("SeeMore_Action - Platform: {0} - Hashtag: {1} - Youtube_Cat: {2} - Tiktok_Cat: {3}".format(platform, hashtag, youtubeCategory, tiktokCategory))
        
        if platform and hashtag:
            result = get_trending_by_hashtag(platform, hashtag)
        
            for video in result:
                dispatcher.utter_message(text=video['title'], attachment=video['play'])
        
        if youtubeCategory:
            results = get_trending_by_category(youtubeCategory)

            for result in results:    
                dispatcher.utter_message(text='{0} - {1}'.format(result['title'], result['image']))

        if tiktokCategory:
            dispatcher.utter_message(text='Những trend mới nhất trên tiktok theo {0} là :'.format(tiktokCategory))
            results = get_tiktok_list_trend_by_category(tiktokCategory)
            for result in results:    
                dispatcher.utter_message(text='{0} - {1}'.format(result['desc'], result['url']))
                dispatcher.utter_attachment(result['videos'][0]['url'])
        
        return []