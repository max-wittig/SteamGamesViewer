from flask import Flask, render_template, url_for, redirect
import os
from steam_helper import *
from game import *

app = Flask(__name__)


def get_api_secret():
    with open(os.path.join(os.path.dirname(__file__), "steam_api_key.txt"), "r") as f:
        return f.read()


@app.route('/user/<username>')
def open_stats_page(username):
    steam_helper = SteamHelper(username, get_api_secret())
    return render_template("profile.html", username=username, total_games=len(steam_helper.games),
                           json_content=Game.games_list_to_json(steam_helper.games))


@app.route('/')
def home():
    return redirect(url_for("static", filename="index.html"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=False, port=4000)
