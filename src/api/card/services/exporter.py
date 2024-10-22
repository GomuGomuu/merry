import json

from api.card.models import Card


def generate_data_cards_for_gemini():
    all_cards = Card.objects.all()
    base_url = "http://172.24.160.1:8000"
    cards = []
    for card in all_cards:
        data = {"api_url": f"{base_url}/cards/{card.slug}/", "name": card.name}
        data.update(card.to_json())

        data["illustrations"] = [
            illustration.to_json() for illustration in card.illustrations.all()
        ]

        cards.append(data)

    with open("cards.json", "w") as f:
        # indent=4 for pretty print
        json.dump(cards, f, indent=4)


def generate_tensorflow_dataset():
    # Generate a dataset for tensorflow
    # export all cards in separate folders, which the name of the folder is the card slug

    import os

    all_cards = Card.objects.all()

    for card in all_cards:
        illustrations = card.illustrations.all()
        for illustration in illustrations:
            try:
                image_file = illustration.src
                image_extension = image_file.name.split(".")[-1]

                folder = f"tensorflow_dataset/{illustration.code}"
                os.makedirs(folder)

                with open(f"{folder}/{illustration.code}.{image_extension}", "wb") as f:
                    f.write(image_file.read())

            except Exception as e:
                print(f"Error on card {card.slug} illustration {illustration.code}: {e}")

    print("Dataset generated")
