from typing import Any, Text, Dict, List
from trending_api import get_trending, get_trending_by_hashtag  
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from tiktokapi import get_tiktok_trending_by_hashtag

import sys
import random
import json

sys.path.insert(0, '../')

class ActionTopTrending(Action):

    def name(self) -> Text:
        return "action_top_trending"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        platform = next(tracker.get_latest_entity_values("platform"),None)

        result = get_trending(platform)
        
        for category in result:
            dispatcher.utter_message(text='{0}: {1} - {2}'.format(category['desc'], category['name'], category['url']))
            # dispatcher.utter_attachment(attachment={
            #     "type": 'video',
            #     "payload": {
            #         "src": video['play']
            #     }
            # })

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
