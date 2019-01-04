import requests
from steamgamesviewer.game import Game
import json


class SteamError(Exception):
    pass


class UserError(Exception):
    pass


class SteamHelper:
    def __init__(self, username, steam_api_key):
        self.steam_username_resolve_url = (
            "http://api.steampowered.com"
            "/ISteamUser/ResolveVanityURL"
            "/v0001/?key=" + str(steam_api_key) + "&vanityurl=" + str(username)
        )
        self.steam_games_url = (
            "http://api.steampowered.com/IPlayerService"
            "/GetOwnedGames/v0001/?key="
            + str(steam_api_key)
            + "&steamid="
            + str(self.steam_id)
            + "&format=json&include_appinfo='true'"
        )
        self.steam_img_url_root = (
            "http://media.steampowered.com" "/steamcommunity" "/public/images/apps/"
        )

    def games(self):
        games_list = []
        request = requests.get(self.steam_games_url, timeout=2)
        if 400 <= request.status_code < 500:
            raise UserError
        if request.status_code >= 500:
            raise SteamError
        response = json.loads(request.text)["response"]
        games_json = response["games"]
        for json_game in games_json:
            current_game = Game(
                json_game["appid"],
                json_game["playtime_forever"],
                str(json_game["name"]),
                self.steam_img_url_root
                + str(json_game["appid"])
                + "/"
                + json_game["img_icon_url"]
                + ".jpg",
            )
            games_list.append(current_game)
        games_list.sort(key=lambda game: game.playtime, reverse=True)
        return games_list

    @property
    def steam_id(self):
        try:
            request = requests.get(self.steam_username_resolve_url)
            return json.loads(request.text)["response"]["steamid"]
        except KeyError:
            return -1
