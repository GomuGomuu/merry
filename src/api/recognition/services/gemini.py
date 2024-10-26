import json

from config import settings
import logging
import google.generativeai as genai
import typing_extensions as typing

logger = logging.getLogger(__name__)


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


class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_URL)

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
