from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
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


class ActionRecommend(Action):

    def name(self) -> Text:
        return "action_recommend"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food = []
        for i in range(2):
            food_number = random.randrange(len(DATABASE))
            food.append(DATABASE[food_number])

        dispatcher.utter_message(
            text="Em nghĩ hôm nay anh chị có thể thử món '{}' hoặc bên cạnh đó cũng có thể là món '{}' ạ".format(food[0], food[1]))

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
