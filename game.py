import json


class Game:
    def __init__(self, app_id, playtime, name, img_icon_url):
        self.app_id = app_id
        self.playtime = playtime
        self.name = name
        self.img_icon_url = img_icon_url

    def to_json(self):
        game = {
            "app_id": self.app_id,
            "playtime": self.playtime,
            "name": self.name,
            "img_icon_url": self.img_icon_url
        }
        return game

    @staticmethod
    def games_list_to_json(games_list):
        json_objects = []
        for current_game in games_list:
            json_objects.append(current_game.to_json())
        return json.dumps(json_objects)
