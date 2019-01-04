import os

from flask import Flask, render_template, Response, request, redirect, url_for
import sys
from steamgamesviewer.steam_account import SteamError, UserError

from steamgamesviewer.game import Game
from steamgamesviewer.steam_account import SteamHelper

app = Flask(__name__)


class ReverseProxied(object):
    """Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get("HTTP_X_SCRIPT_NAME", "")
        if script_name:
            environ["SCRIPT_NAME"] = script_name
            path_info = environ["PATH_INFO"]
            if path_info.startswith(script_name):
                environ["PATH_INFO"] = path_info[len(script_name):]

        scheme = environ.get("HTTP_X_SCHEME", "")
        if scheme:
            environ["wsgi.url_scheme"] = scheme
        return self.app(environ, start_response)


@app.route("/user", methods=["GET"])
def redirect_to_stats():
    return redirect(
        url_for("open_stats_page", username=str(request.args.get("username")))
    )


@app.route("/user/<username>")
def open_stats_page(username):
    username = str(username)
    steam_helper = SteamHelper(username, os.getenv("STEAM_API_KEY"))
    try:
        games = steam_helper.games()

        return render_template(
            "profile.html",
            username=username,
            total_games=len(games),
            json_content=Game.games_list_to_json(games),
        )
    except UserError:
        return render_template(
            "error.html",
            reason="User not found!"
        )
    except SteamError:
        return render_template(
            "error.html",
            reason="Could not access user. The profile might be set to private."
        )
    except KeyError:
        return render_template(
            "error.html",
            reason="Error, while parsing json output!"
        )


@app.route("/")
def home():
    return render_template("index.html")


def main():
    if not os.getenv("STEAM_API_KEY"):
        sys.exit("Please set the STEAM_API_KEY environment variable!")
    app.wsgi_app = ReverseProxied(app.wsgi_app)
    app.run(host="0.0.0.0", debug=False, port=4000)


if __name__ == "__main__":
    main()
