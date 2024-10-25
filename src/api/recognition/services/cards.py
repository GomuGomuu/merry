import json
import os
from sentence_transformers import SentenceTransformer, util

import logging

from config.settings import BASE_DIR

logger = logging.getLogger(__name__)


class CardMatcher:
    def __init__(
        self,
        model_name="paraphrase-MiniLM-L6-v2",
        embedded_cards_file_path=f"{BASE_DIR}/api/recognition/embeddings/cards.json",
    ):
        self.model = SentenceTransformer(model_name)
        self.embedded_cards_file_path = embedded_cards_file_path
        self.embedded_cards = self.get_embeddings()

    def _create_card_embedding(self, card):
        logger.info(f"Creating card embedding for {card.name}")
        texts = [
            card.name,
            card.effect,
            (
                " ".join(crew.name for crew in card.crew.all())
                if card.crew.exists()
                else ""
            ),
            card.type,
            str(card.power),
            str(card.cost),
        ]
        card_text = " ".join(filter(None, texts))
        return self.model.encode(card_text)

    def _create_extracted_embedding(self, extracted_data):
        texts = [
            extracted_data.get("attack"),
            extracted_data.get("cost"),
            extracted_data.get("description"),
            extracted_data.get("name"),
            extracted_data.get("tribe"),
            extracted_data.get("type"),
        ]
        extracted_text = " ".join([text for text in texts if text])
        return self.model.encode(extracted_text)

    def get_embeddings(self):
        if os.path.exists(self.embedded_cards_file_path):
            logger.info("Cache already exists")
            with open(self.embedded_cards_file_path, "r", encoding="utf-8") as f:
                cached_embeddings = json.load(f)
                return cached_embeddings
        else:
            logger.info("Creating cache")
            cached_embeddings = {}

        from api.card.models import Card

        cards = Card.objects.all()
        for card in cards:
            card_embedding = self._create_card_embedding(card).tolist()
            cached_embeddings[card.slug] = card_embedding

        with open(self.embedded_cards_file_path, "w", encoding="utf-8") as f:
            json.dump(cached_embeddings, f)

        logger.info("Cache created")
        return cached_embeddings

    def find_closest_card(self, extracted_data, cached_embeddings=None):
        logger.info("Finding closest card")
        extracted_embedding = self._create_extracted_embedding(extracted_data)

        if cached_embeddings is None:
            logger.info("Loading embeddings cache")
            with open(self.embedded_cards_file_path, "r", encoding="utf-8") as f:
                cached_embeddings = json.load(f)

        best_match = {"card_slug": None, "similarity": -1}
        best_similarity = -1

        for card in self.embedded_cards:
            card_embedding = cached_embeddings[card["slug"]]
            similarity = util.pytorch_cos_sim(
                extracted_embedding, card_embedding
            ).item()

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = {"card_slug": card["slug"], "similarity": similarity}

        logger.info(f"Best match found: {best_match}")
        return best_match

    def find_closest_cards(self, extracted_data, cached_embeddings=None, top_n=5):
        logger.info("Finding closest cards")
        extracted_embedding = self._create_extracted_embedding(extracted_data)

        if cached_embeddings is None:
            logger.info("Loading embeddings cache")
            with open(self.embedded_cards_file_path, "r", encoding="utf-8") as f:
                cached_embeddings = json.load(f)

        similarities = []

        for card in self.embedded_cards:
            card_embedding = cached_embeddings[card["slug"]]
            similarity = util.pytorch_cos_sim(
                extracted_embedding, card_embedding
            ).item()

            similarities.append({"card_slug": card["slug"], "similarity": similarity})

        similarities = sorted(similarities, key=lambda x: x["similarity"], reverse=True)

        top_matches = similarities[:top_n]

        top_cards = [
            {**match["card_slug"], "confidence": match["similarity"]}
            for match in top_matches
        ]

        logger.info(f"Matches found: {top_cards}")
        return top_cards
