import logging
import pathlib
from typing import Any, Dict, List, Text, Type
import os
import gzip

import fasttext
import numpy as np
from rasa.engine.graph import ExecutionContext, GraphComponent
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.nlu.constants import DENSE_FEATURIZABLE_ATTRIBUTES
from rasa.nlu.featurizers.dense_featurizer.dense_featurizer import DenseFeaturizer
from rasa.nlu.tokenizers.tokenizer import Tokenizer
from rasa.shared.nlu.constants import (
    FEATURE_TYPE_SENTENCE,
    FEATURE_TYPE_SEQUENCE,
    TEXT,
    TEXT_TOKENS,
)
from rasa.shared.nlu.training_data.features import Features
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData

logger = logging.getLogger(__name__)


@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.MESSAGE_FEATURIZER, is_trainable=False
)
class FastTextFeaturizer(DenseFeaturizer, GraphComponent):
    """This component adds fasttext features."""

    @classmethod
    def required_components(cls) -> List[Type]:
        """Components that should be included in the pipeline before this component."""
        return [Tokenizer]

    @staticmethod
    def required_packages() -> List[Text]:
        """Any extra python dependencies required for this component to run."""
        return ["fasttext"]

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        """Returns the component's default config."""
        return {
            **DenseFeaturizer.get_default_config(),
            # specifies the language of the subword segmentation model
            "cache_path": None,
        }

    def __init__(
        self,
        config: Dict[Text, Any],
        name: Text,
    ) -> None:
        """Constructs a new byte pair vectorizer."""
        self.validate_config(config)
        self.alias = name if not config.get("alias") else config["alias"]
        # The configuration dictionary is saved in `self._config` for reference.
        path = config["cache_path"]
        self.model = fasttext.load_model(path)

    @classmethod
    def create(
        cls,
        config: Dict[Text, Any],
        model_storage: ModelStorage,
        resource: Resource,
        execution_context: ExecutionContext,
    ) -> GraphComponent:
        """Creates a new component (see parent class for full docstring)."""
        return cls(config, execution_context.node_name)

    def process(self, messages: List[Message]) -> List[Message]:
        """Processes incoming messages and computes and sets features."""
        for message in messages:
            for attribute in DENSE_FEATURIZABLE_ATTRIBUTES:
                self._set_features(message, attribute)
        return messages

    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        """Processes the training examples in the given training data in-place."""
        self.process(training_data.training_examples)
        return training_data

    def _create_word_vector(self, document: Text) -> np.ndarray:
        """Creates a word vector from a text. Utility method."""
        return self.model.get_word_vector(document)

    def _set_features(self, message: Message, attribute: Text = TEXT) -> None:
        """Sets the features on a single message. Utility method."""
        tokens = message.get(TEXT_TOKENS)

        # If the message doesn't have tokens, we can't create features.
        if not tokens:
            return None

        # We need to reshape here such that the shape is equivalent to that of sparsely
        # generated features. Without it, it'd be a 1D tensor. We need 2D (n_utterance, n_dim).
        text_vector = self._create_word_vector(document=message.get(TEXT)).reshape(
            1, -1
        )
        word_vectors = np.array(
            [self._create_word_vector(document=t.text) for t in tokens]
        )

        final_sequence_features = Features(
            word_vectors,
            FEATURE_TYPE_SEQUENCE,
            attribute,
            self.alias,
        )
        message.add_features(final_sequence_features)
        final_sentence_features = Features(
            text_vector,
            FEATURE_TYPE_SENTENCE,
            attribute,
            self.alias,
        )
        message.add_features(final_sentence_features)

    @classmethod
    def validate_config(cls, config: Dict[Text, Any]) -> None:
        """Validates that the component is configured properly."""
        if "cache_path" not in config.keys():
            raise ValueError(
                "FastTextFeaturizer needs pre-trained cache file `cache_path`."
            )
        if not pathlib.Path(config["cache_path"]).exists():
            raise FileNotFoundError(
                f"FastTextFeaturizer `cache_path={config['cache_path']}` does not exist."
            )