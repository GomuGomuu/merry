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
        embedded_illustrations_file_path: str = f"{BASE_DIR}/api/recognition/embeddings/embedded_illustrations.json",
        card_data_file_path: str = f"{BASE_DIR}/api/recognition/embeddings/card_data.json",
    ):
        self.model = SentenceTransformer(model_name)
        self.embedded_cards_file_path = embedded_cards_file_path
        self.embedded_cards = {}
        self.embedded_illustrations_file_path = embedded_illustrations_file_path
        self.embedded_illustrations = {}
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

    def _create_illustrations_embedding(self, card):
        logger.info(f"Creating illustrations embedding for {card.name}")
        illustrations = card.illustrations.all()
        if illustrations.exists():
            illustrations_embedding = {}
            for illustration in illustrations:
                data = json.dumps(illustration.visual_description["data"])

                illustration_embedding = self.model.encode(data)
                illustrations_embedding[illustration.code] = (
                    illustration_embedding.tolist()
                )

            self.embedded_illustrations[card.slug] = illustrations_embedding

    def _extract_card_embedding(self, extracted_data):
        texts = [
            extracted_data.get("name"),
            extracted_data.get("description"),
            extracted_data.get("crew"),
            extracted_data.get("type"),
        ]
        extracted_text = " ".join([text for text in texts if text])
        return self.model.encode(extracted_text)

    def _extrac_visual_description_embedding(self, extracted_data):
        data = extracted_data.get("layout_description")
        if data is None:
            return self.model.encode("Default visual description")
        texts = [
            data.get("background_color"),
            data.get("border_color"),
            data.get("dominant_color"),
            data.get("illustration_description"),
        ]
        extracted_text = " ".join([text for text in texts if text])
        return self.model.encode(extracted_text)

    def _load_data_files(self):
        if (
            os.path.exists(self.embedded_cards_file_path)
            and os.path.exists(self.card_data_file_path)
            and os.path.exists(self.embedded_illustrations_file_path)
        ):
            logger.info("Loading cached embeddings and card data")
            with open(self.embedded_cards_file_path, "r", encoding="utf-8") as f:
                self.embedded_cards = json.load(f)
            with open(self.card_data_file_path, "r", encoding="utf-8") as f:
                self.card_data = json.load(f)
            with open(
                self.embedded_illustrations_file_path, "r", encoding="utf-8"
            ) as f:
                self.embedded_illustrations = json.load(f)
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
            self._create_illustrations_embedding(card)

        os.makedirs(os.path.dirname(self.embedded_cards_file_path), exist_ok=True)
        with open(self.card_data_file_path, "w", encoding="utf-8") as f:
            json.dump(self.card_data, f, ensure_ascii=False, indent=4)

        os.makedirs(os.path.dirname(self.embedded_cards_file_path), exist_ok=True)
        with open(self.embedded_cards_file_path, "w", encoding="utf-8") as f:
            json.dump(self.embedded_cards, f, ensure_ascii=False, indent=4)

        os.makedirs(
            os.path.dirname(self.embedded_illustrations_file_path), exist_ok=True
        )
        with open(self.embedded_illustrations_file_path, "w", encoding="utf-8") as f:
            json.dump(self.embedded_illustrations, f, ensure_ascii=False, indent=4)

    def find_closest_card(self, extracted_data, cached_embeddings=None):
        logger.info("Finding closest card...")
        extracted_card_embedding = self._extract_card_embedding(extracted_data)
        visual_description_embedding = self._extrac_visual_description_embedding(
            extracted_data
        )

        if cached_embeddings is None:
            logger.info("Loading embeddings from cache")
            with open(self.embedded_cards_file_path, "r", encoding="utf-8") as f:
                cached_embeddings = json.load(f)

        best_match = {"card_slug": None, "similarity": -1}

        for slug, card_embedding in cached_embeddings.items():
            similarity = util.cos_sim(extracted_card_embedding, card_embedding).item()
            if similarity > best_match["similarity"]:
                best_match = {"card_slug": slug, "similarity": similarity}

        illustration_positions = []

        for illustration in self.embedded_illustrations[best_match["card_slug"]]:
            illustration_embedding = self.embedded_illustrations[
                best_match["card_slug"]
            ][illustration]
            similarity = util.cos_sim(
                visual_description_embedding, illustration_embedding
            ).item()
            illustration_positions.append(
                {"code": illustration, "similarity": similarity}
            )

        illustration_positions = sorted(
            illustration_positions, key=lambda x: x["similarity"], reverse=True
        )

        best_match["illustrations"] = illustration_positions

        return best_match

    def find_closest_cards(self, extracted_data, top_n=5):
        logger.info("Finding closest cards...")
        extracted_card_embedding = self._extract_card_embedding(extracted_data)
        visual_description_embedding = self._extrac_visual_description_embedding(
            extracted_data
        )

        similarities = []

        for card in self.card_data:
            card_embedding = self.embedded_cards[card["slug"]]
            similarity = util.cos_sim(extracted_card_embedding, card_embedding).item()
            similarities.append({"card_slug": card["slug"], "similarity": similarity})

        similarities = sorted(similarities, key=lambda x: x["similarity"], reverse=True)

        top_matches = similarities[:top_n]
        top_cards = [
            {
                "slug": match["card_slug"],
                "similarity": match["similarity"],
                "illustrations": [],
            }
            for match in top_matches
        ]

        logger.info(f"Top {top_n} matches found: {top_cards}")

        for match in top_cards:
            illustration_positions = []

            illustrations_embedding = self.embedded_illustrations[match["slug"]]

            for illustration in illustrations_embedding:
                illustration_embedding = illustrations_embedding[illustration]
                similarity = util.cos_sim(
                    visual_description_embedding, illustration_embedding
                ).item()
                illustration_positions.append(
                    {"code": illustration, "similarity": similarity}
                )

            illustration_positions = sorted(
                illustration_positions, key=lambda x: x["similarity"], reverse=True
            )

            match["illustrations"] = illustration_positions

        return top_cards
