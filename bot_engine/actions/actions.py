from typing import Any, Text, Dict, List
import sys
  
sys.path.insert(0, '../')

from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
from tiktokapi import get_tiktok_trending, get_tiktok_trending_by_hashtag, get_trending
import random
import json

class ActionTopTrending(Action):

    def name(self) -> Text:
        return "action_top_trending"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        result = get_trending()
        for category in result:
            # dispatcher.utter_message(text='{0}: {1}'.format(video['desc'], video['name']))
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

        hashtag = tracker.get_slot("hashtag")
        result = get_tiktok_trending_by_hashtag(hashtag)
        for video in result:
            dispatcher.utter_message(text=video['title'], image=video['cover'])

        return []
