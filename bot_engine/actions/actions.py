import sys
import random
import json
import requests

sys.path.insert(0, '../')

from recommend_service.user import user_vote

from typing import Any, Text, Dict, List
from trending_api import get_more_youtube_trending, get_trending, get_trending_by_category, get_trending_by_hashtag 
from tiktok_api import get_tiktok_list_trend_by_category, get_tiktok_trending

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet



class GetName(Action):
    def name(self):
        return 'action_name'
    
    def run(self, dispatcher, tracker, domain):
        
        #Enable when using messeger
        most_recent_state = tracker.current_state()
        
        sender_id = most_recent_state['sender_id']
        
        r = requests.get('https://graph.facebook.com/{}?fields=first_name,last_name,profile_pic&access_token={}'.format(sender_id, fb_access_token)).json()
        
        first_name = r['first_name'] 
        last_name = r['last_name'] 
        
        #Default
        #first_name = 'Rasa'
        #last_name = 'Shell'
        
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
            
        return [SlotSet('platform', 'tiktok')]

class ActionTopTrendingYoutube(Action):
    
    def name(self) -> Text:
        return "action_top_trending_youtube"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("TopTrendingYoutube_Action")
        
        most_recent_state = tracker.current_state()
        
        sender_id = most_recent_state['sender_id']
        
        results = get_trending(sender_id)

        for result in results:
                videolink = 'https://www.youtube.com/watch?v={0}'.format(result['id'])    
                dispatcher.utter_message(text='{0}'.format(result['title']))
                dispatcher.utter_message(videolink)
        return [SlotSet('platform', 'youtube'), SlotSet('youtubeCategory', None), SlotSet('hashtag', None)]

class ActionTrendingByHashTag(Action):

    def name(self) -> Text:
        return "action_trending_by_hashtag"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        platform = tracker.get_slot("platform")
        hashtag = tracker.get_slot("hashtag")

        most_recent_state = tracker.current_state()
        
        sender_id = most_recent_state['sender_id']

        print("TrendingByHashTag_Action - Platform: {0} - Hashtag: {1}".format(platform, hashtag))
        
        result = get_trending_by_hashtag(platform, hashtag, sender_id)
        
        dispatcher.utter_message(text='Những video xu hướng theo từ khóa {0} trên nền tảng {1} là'.format(hashtag, platform))
        for video in result:
            if(platform == 'tiktok'):
                dispatcher.utter_message(text=video['title'], attachment=video['play'])
            else:
                videolink = 'https://www.youtube.com/watch?v={0}'.format(video['id'])    
                dispatcher.utter_message(text='{0}'.format(video['title']))
                dispatcher.utter_message(videolink)
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
                dispatcher.utter_message(text='{0} - {1}'.format(result['name'], result['url']))
                dispatcher.utter_attachment(result['videos'][0]['url'])
        else:
            dispatcher.utter_message(text="Em chưa hiểu thể loại anh/chị muốn chọn, vui lòng chọn lại ạ!")
            
        return [SlotSet('platform', 'tiktok')]

class ActionTrendingByYoutubeCategory(Action):

    def name(self) -> Text:
        return "action_top_youtube_trending_by_category"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        youtubeCategory = next(tracker.get_latest_entity_values("youtubeCategory"),None)
        
        print("TrendingByYoutubeCategory_Action - Category: {0}".format(youtubeCategory))
        
        most_recent_state = tracker.current_state()
        
        sender_id = most_recent_state['sender_id']
        
        results = get_trending_by_category(youtubeCategory, sender_id)

        for result in results:    
                videolink = 'https://www.youtube.com/watch?v={0}'.format(result['id'])    
                dispatcher.utter_message(text='{0}'.format(result['title']))
                dispatcher.utter_message(videolink)
            
        return [SlotSet('youtubeCategory', youtubeCategory), SlotSet('platform', 'youtube'), SlotSet('hashtag', None)]
    
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
        
        most_recent_state = tracker.current_state()
        
        sender_id = most_recent_state['sender_id']
        
        if platform == 'tiktok' and hashtag:
            result = get_trending_by_hashtag(platform, hashtag)
        
            for video in result:
                dispatcher.utter_message(text=video['title'], attachment=video['play'])
            
            return []
        
        if platform == 'youtube':

            results = get_more_youtube_trending(sender_id)
            
            for result in results:    
                #dispatcher.utter_message(text='{0} - {1}'.format(result['title'], result['image']))
                videolink = 'https://www.youtube.com/watch?v={0}'.format(result['id'])    
                dispatcher.utter_message(text='{0}'.format(result['title']))
                dispatcher.utter_message(videolink)
                
            return []

        if tiktokCategory:
            dispatcher.utter_message(text='Những trend mới nhất trên tiktok theo {0} là :'.format(tiktokCategory))
            results = get_tiktok_list_trend_by_category(tiktokCategory)
            for result in results:    
                dispatcher.utter_message(text='{0} - {1}'.format(result['desc'], result['url']))
                dispatcher.utter_attachment(result['videos'][0]['url'])
        
        return []
    
class ActionTrendIsBad(Action):
    
    def name(self) -> Text:
        return "action_trend_is_bad"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text='Xin lỗi bạn, mình sẽ cố gắng hơn')
        
        print("TrendIsBad_Action")
        
        most_recent_state = tracker.current_state()
        
        sender_id = most_recent_state['sender_id']
        
        user_vote(sender_id, random.choice([0, 1]))
        
        return []

class ActionTrendIsNormal(Action):
    
    def name(self) -> Text:
        return "action_trend_is_normal"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text='Cảm ơn bạn, chúc bạn một ngày tốt lành')
        
        print("TrendIsNormal_Action")
        
        most_recent_state = tracker.current_state()
        
        sender_id = most_recent_state['sender_id']
        
        user_vote(sender_id, random.choice([2, 3]))
        
        return []

class ActionTrendIsGood(Action):
    
    def name(self) -> Text:
        return "action_trend_is_good"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text='Cảm ơn bạn nhiều, bot sẽ cải thiện và giúp đỡ bạn nhiều hơn')
        
        print("TrendIsGood_Action")
                
        most_recent_state = tracker.current_state()
        
        sender_id = most_recent_state['sender_id']
        
        user_vote(sender_id, random.choice([4, 5]))
        
        return []