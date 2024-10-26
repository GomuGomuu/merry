import json
import os
from sentence_transformers import SentenceTransformer, util
import logging
from config.settings import BASE_DIR

logger = logging.getLogger(__name__)


class CardMatcher:
    def __init__(
        self,
        model_name: str = "paraphrase-MiniLM-L6-v2",
        embedded_cards_file_path: str = f"{BASE_DIR}/api/recognition/embeddings/embedded_cards.json",
        card_data_file_path: str = f"{BASE_DIR}/api/recognition/embeddings/card_data.json",
    ):
        self.model = SentenceTransformer(model_name)
        self.embedded_cards_file_path = embedded_cards_file_path
        self.embedded_cards = {}
        self.card_data_file_path = card_data_file_path
        self.card_data = None
        self._load_data_files()

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
        card_text = " ".join([text for text in texts if text])
        card_embedding = self.model.encode(card_text)
        self.embedded_cards[card.slug] = card_embedding.tolist()
        return card_embedding

    def _create_card_data(self, card):
        logger.info(f"Creating card data for {card.name}")
        card_data = card.to_json()
        self.card_data = self.card_data or []
        self.card_data.append(card_data)

    def _create_extracted_embedding(self, extracted_data):
        texts = [
            extracted_data["name"],
            extracted_data["description"],
            extracted_data["crew"],
            extracted_data["type"],
        ]
        extracted_text = " ".join([text for text in texts if text])
        return self.model.encode(extracted_text)

    def _load_data_files(self):
        if os.path.exists(self.embedded_cards_file_path) and os.path.exists(
            self.card_data_file_path
        ):
            logger.info("Loading cached embeddings and card data")
            with open(self.embedded_cards_file_path, "r", encoding="utf-8") as f:
                self.embedded_cards = json.load(f)
            with open(self.card_data_file_path, "r", encoding="utf-8") as f:
                self.card_data = json.load(f)
        else:
            logger.info("Cache not found, creating new data files...")
            self.update_data_files()

    def update_data_files(self):
        """Force update the card data and embeddings files."""
        from api.card.models import Card

        self.card_data = []
        self.embedded_cards = {}

        cards = Card.objects.all()
        for card in cards:
            self._create_card_data(card)
            self._create_card_embedding(card)

        os.makedirs(os.path.dirname(self.embedded_cards_file_path), exist_ok=True)
        with open(self.card_data_file_path, "w", encoding="utf-8") as f:
            json.dump(self.card_data, f, ensure_ascii=False, indent=4)

        with open(self.embedded_cards_file_path, "w", encoding="utf-8") as f:
            json.dump(self.embedded_cards, f, ensure_ascii=False, indent=4)

    def find_closest_card(self, extracted_data, cached_embeddings=None):
        logger.info("Finding closest card...")
        extracted_embedding = self._create_extracted_embedding(extracted_data)

        if cached_embeddings is None:
            logger.info("Loading embeddings from cache")
            with open(self.embedded_cards_file_path, "r", encoding="utf-8") as f:
                cached_embeddings = json.load(f)

        best_match = {"card_slug": None, "similarity": -1}

        for slug, card_embedding in cached_embeddings.items():
            similarity = util.cos_sim(extracted_embedding, card_embedding).item()
            if similarity > best_match["similarity"]:
                best_match = {"card_slug": slug, "similarity": similarity}

        logger.info(f"Best match found: {best_match}")
        return best_match

    def find_closest_cards(self, extracted_data, top_n=5):
        logger.info("Finding closest cards...")
        extracted_embedding = self._create_extracted_embedding(extracted_data)

        similarities = []

        for card in self.card_data:
            card_embedding = self.embedded_cards[card["slug"]]
            similarity = util.cos_sim(extracted_embedding, card_embedding).item()
            similarities.append({"card_slug": card["slug"], "similarity": similarity})

        similarities = sorted(similarities, key=lambda x: x["similarity"], reverse=True)

        top_matches = similarities[:top_n]
        top_cards = [
            {
                "slug": match["card_slug"],
                "similarity": match["similarity"],
            }
            for match in top_matches
        ]

        logger.info(f"Top matches found: {top_cards}")

        return top_cards
