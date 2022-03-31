from __future__ import annotations

from typing import Any, Dict, List, Optional, Text
from rasa.nlu.tokenizers.tokenizer import Token, Tokenizer
from rasa.shared.nlu.training_data.message import Message

from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.nlu.constants import TOKENS_NAMES, MESSAGE_ATTRIBUTES
from rasa.engine.graph import ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage

@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.MESSAGE_TOKENIZER, is_trainable=False
)
class VietnameseTokenizer(Tokenizer):

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        """Returns the component's default config."""
        return {
            # This *must* be added due to the parent class.
            "intent_tokenization_flag": False,
            # This *must* be added due to the parent class.
            "intent_split_symbol": "_",
            # This is the spaCy language setting.
            "case_sensitive": True,
        }

    def __init__(self, component_config: Dict[Text, Any]) -> None:
        super().__init__(component_config)
        if component_config.get('tokenizer') == 'underthesea':
            self.tokenizer = 'underthesea'
        else:
            self.tokenizer = 'pyvi'

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> VietnameseTokenizer:
        return cls(config)

    def tokenize(self, message: Message, attribute: Text) -> List[Token]:
        text = message.get(attribute)
        text = text.replace('òa', 'oà').replace('óa', 'oá').replace('ỏa', 'oả').replace('õa', 'oã').replace('ọa', 'oạ').replace('òe', 'oè').replace('óe', 'oé').replace('ỏe', 'oẻ').replace('õe', 'oẽ').replace('ọe', 'oẹ').replace('ùy', 'uỳ').replace('úy', 'uý').replace('ủy', 'uỷ').replace('ũy', 'uỹ').replace('ụy', 'uỵ')
        if self.tokenizer == 'underthesea':
            from underthesea import word_tokenize
            words = word_tokenize(text, format="text").split()
        else:
            from pyvi import ViTokenizer
            words = ViTokenizer.tokenize(text).split()
        text = ' '.join(words)

        return self._convert_words_to_tokens(words, text)
