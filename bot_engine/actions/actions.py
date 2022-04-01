from typing import Any, Text, Dict, List
import sys
  
sys.path.insert(0, '../')

from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher
from tiktokapi import get_tiktok_trending, get_tiktok_trending_by_hashtag
import random
import json

DATABASE = ["bún đậu mắm tôm",
            "bún đậu nước mắm",
            "bún cá",
            "bún hải sản",
            "cơm văn phòng",
            "cơm sườn",
            "xôi",
            "bún ốc",
            "mì vằn thắn",
            "hủ tiếu",
            "bún chả",
            "bún ngan",
            "ngan xào tỏi",
            "bún bò huế",
            "mì tôm hải sản",
            "bánh mì trứng xúc xích rắc thêm ít ngải cứu",
            "bánh mì trứng",
            "bánh mì xúc xích",
            "bánh mì pate"]


class ActionTopTrending(Action):

    def name(self) -> Text:
        return "action_top_trending"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        result = get_tiktok_trending()
        for video in result:
            dispatcher.utter_message(text=video['title'], image=video['cover'])
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
            # dispatcher.utter_attachment(attachment={
            #     "type": 'video',
            #     "payload": {
            #         "src": video['play']
            #     }
            # })

        return []

class ActionAddToDatabase(Action):

    def name(self) -> Text:

        return "action_add_to_database"

    def run(self, dispatcher: CollectingDispatcher,

            tracker: Tracker,

            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entity_location = next(tracker.get_latest_entity_values(entity_type="location"), None)

        entity_db_item_name = next(

            tracker.get_latest_entity_values(entity_type="location", entity_role="to_database"), None)

        with open('utils/database.json', 'r', encoding = 'utf-8') as db:

            database = json.load(db)

        database.update({entity_db_item_name: entity_location})

        with open('utils/database.json', 'w', encoding = 'utf-8') as db:

            json.dump(database, db)

        return []
