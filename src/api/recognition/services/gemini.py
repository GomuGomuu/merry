import json

from config import settings
import logging
import google.generativeai as genai
import typing_extensions as typing

logger = logging.getLogger(__name__)


class CardLayoutDescription(typing.TypedDict):
    illustration_description: str
    number_of_persons: int
    background_color: str
    border_color: str
    dominant_color: str


class CardResponseFormat(typing.TypedDict):
    life: int
    attack: int
    cost: int
    counter: int
    type: str
    name: str
    crew: str
    description: str
    trigger: str
    layout_description: CardLayoutDescription


class GeminiService:
    def __init__(self, api_key: str = None):
        genai.configure(api_key=api_key or settings.GEMINI_API_KEY)

    @classmethod
    def get_card_text_from_image(
        cls, image_path: str
    ) -> typing.Optional[CardResponseFormat]:
        try:
            logger.info(f"Uploading image: {image_path} to Gemini")
            card_file = genai.upload_file(image_path)
            model = genai.GenerativeModel("gemini-1.5-flash")

            logger.info(f"Extracting text from image: {image_path}")
            response = model.generate_content(
                [
                    "You are a expert extracting text from images.",
                    "Extract the maximum text possible from this image.",
                    "Do not generate random values, just extract the text from the image.",
                    "And, create a description what you see in the image with details, "
                    "like colors, shapes, etc.",
                    "Send me JSON format",
                    card_file,
                ],
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=CardResponseFormat,
                ),
            )

            logger.info("Text extracted from image")

            return json.loads(response.text)

        except Exception as e:
            logger.error(f"Error extracting text from image: {e}")
            return None

    @classmethod
    def get_description_from_image(
        cls, image_path: str
    ) -> typing.Optional[CardLayoutDescription]:
        try:
            logger.info(f"Uploading image: {image_path} to Gemini")
            card_file = genai.upload_file(image_path)
            model = genai.GenerativeModel("gemini-1.5-flash")

            logger.info(f"Analyzing image: {image_path}")
            response = model.generate_content(
                [
                    "You are a expert analyzing images.",
                    "Create a description what you see in the image with details, "
                    "like colors, shapes, etc.",
                    "Send me JSON format",
                    card_file,
                ],
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=CardLayoutDescription,
                ),
            )

            logger.info("Image analyzed")

            return json.loads(response.text)

        except Exception as e:
            logger.error(f"Error extracting text from image: {e}")
            return None
