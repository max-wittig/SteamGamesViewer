from flask import Flask, render_template, url_for, redirect, Response
import os
from steam_account import SteamHelper
from game import Game

app = Flask(__name__)


@app.route('/user/<username>')
def open_stats_page(username):
    username = str(username)
    steam_helper = SteamHelper(username, os.getenv("STEAM_API_KEY"))
    if not steam_helper.games:
        return Response("User not found!", 404)
    return render_template(
        "profile.html", username=username, total_games=len(
            steam_helper.games), json_content=Game.games_list_to_json(
            steam_helper.games))


@app.route('/')
def home():
    return redirect(url_for("static", filename="index.html"))


if __name__ == '__main__':
    if not os.getenv("STEAM_API_KEY"):
        exit("Please set the STEAM_API_KEY environment variable!")
    app.run(host="0.0.0.0", debug=False, port=4000)
