import sys
import random
import json

sys.path.insert(0, '../')

from typing import Any, Text, Dict, List
from trending_api import get_trending, get_trending_by_hashtag  
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

class ActionTopTrending(Action):

    def name(self) -> Text:
        return "action_top_trending"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        platform = next(tracker.get_latest_entity_values("platform"),None)
        print("Platform is", platform)

        results = get_trending(platform)
        
        if(platform == "tiktok"):
        
            for category in results:
                dispatcher.utter_message(text='{0}: {1} - {2}'.format(category['desc'], category['name'], category['url']))
        else:
            for result in results:    
                dispatcher.utter_message(text='{0} - {1}'.format(result['title'], result['image']))
            
        return []

class ActionTrendingByHashTag(Action):

    def name(self) -> Text:
        return "action_trending_by_hashtag"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        hashtag = next(tracker.get_latest_entity_values("hashtag"),None)
        platform = next(tracker.get_latest_entity_values("platform"),None)
        
        print("Hashtag is", hashtag)
        print("Platform is", platform)
        
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
    
class ValidatePlatformSelected(FormValidationAction):
    def name(self) -> Text:
        return "validate_platform_select"
    def validate_platform(self, slot_value: Any, 
                          dispatcher: CollectingDispatcher, 
                          tracker: Tracker, 
                          domain: DomainDict):
        
        if(slot_value == "tiktok" or slot_value == "youtube"):
            dispatcher.utter_message(text='Platform is: {0} '.format(slot_value))
            return {"platform" : slot_value}
                                  
        return {"platform": None}
