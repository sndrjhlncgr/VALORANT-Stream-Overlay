import urllib

from flask import Flask, Response, render_template, make_response, request
from dotenv import load_dotenv, find_dotenv
import os, socket
import requests

hostname = socket.gethostname()

load_dotenv(find_dotenv())

CLIENT_IP = socket.gethostbyname(hostname)
AUTHORIZATION = 'https://auth.riotgames.com/api/v1/authorization'

RIOT_USERNAME = os.getenv("RIOT_USERNAME")
RIOT_PASSWORD = os.getenv("RIOT_PASSWORD")
USER_REGION = os.getenv("USER_REGION")

app = Flask(__name__, template_folder="components")


def getCookies():
    credentials = {
        'client_id': 'play-valorant-web-prod',
        'nonce': '1',
        'redirect_uri': 'https://playvalorant.com/',
        'response_type': 'token id_token',
        'scope': 'account openid',
    }

    headers = {
        'X-Forwarded-For': f'{CLIENT_IP}'
    }
    response = requests.post(AUTHORIZATION, headers=headers, json=credentials)
    cookies = response.cookies
    return cookies


def getAccessToken():
    cookies = getCookies()
    credentials = {
        'type': 'auth',
        'username': RIOT_USERNAME,
        'password': RIOT_PASSWORD
    }
    headers = {
        'X-Forwarded-For': f'{CLIENT_IP}'
    }
    response = requests.put(AUTHORIZATION, headers=headers, json=credentials, cookies=cookies)

    # WHAT IF WRONG USERNAME AND PASSWORD -> FIXING....

    uri = response.json()['response']['parameters']['uri']
    access_token = urllib.parse.parse_qs(uri)
    access_token = access_token['https://playvalorant.com/#access_token'][0]
    return access_token


@app.route('/')
def start():
    data = {

    }
    return render_template("valorantRank.html.j2", **data)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    data = start()

    response = Response(data, mimetype="image/svg+xml")
    response.headers["Cache-Control"] = "s-maxage=1"

    return response


if __name__ == '__main__':
    app.run(debug=True)
