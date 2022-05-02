from rasa.nlu.components import Component
from rasa.nlu import utils
from rasa.nlu.model import Metadata
from underthesea import sentiment
import os

class SentimentAnalyzer(Component):

    name = "sentiment"
    provides = ["entities"]
    requires = []
    defaults = {}
    language_list = ["vi"]

    def __init__(self, component_config=None):
        super(SentimentAnalyzer, self).__init__(component_config)

    def convert_to_rasa(self, value, confidence):
        """Convert model output into the Rasa NLU compatible output format."""
        
        entity = {"value": value,
                  "confidence": confidence,
                  "entity": "sentiment",
                  "extractor": "sentiment_extractor"}

        return entity


    def process(self, message, **kwargs):

        key, confidence = sentiment(message.text), 0.5
        entity = self.convert_to_rasa(key, confidence)
        message.set("entities", [entity], add_to_output=True)