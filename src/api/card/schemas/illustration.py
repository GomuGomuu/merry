from dataclasses import dataclass


@dataclass
class IllustrationVisualDescription:
    def __init__(self, data: dict):
        self.data = data

    @property
    def background_color(self):
        return self.data.get("background_color")

    @property
    def border_color(self):
        return self.data.get("border_color")

    @property
    def dominant_color(self):
        return self.data.get("dominant_color")

    @property
    def illustration_description(self):
        return self.data.get("illustration_description")

    @property
    def number_of_persons(self):
        return self.data.get("number_of_persons")

    @classmethod
    def from_dict(cls, data) -> "IllustrationVisualDescription":
        return IllustrationVisualDescription(data=data)

    def to_dict(self):
        return {
            "data": self.data,
        }
