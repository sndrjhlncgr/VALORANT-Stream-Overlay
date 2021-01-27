import os
import socket
import urllib

import requests
from dotenv import load_dotenv, find_dotenv
from flask import Flask, Response, render_template, make_response

hostname = socket.gethostname()
load_dotenv(find_dotenv())

AUTHORIZATION = 'https://auth.riotgames.com/api/v1/authorization'
ENTITLEMENT_TOKEN_LINK = 'https://entitlements.auth.riotgames.com/api/token/v1'
AUTHORIZATION_INFORMATION = 'https://auth.riotgames.com/userinfo'

CLIENT_PLATFORM = 'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9'

RIOT_USERNAME = os.getenv("RIOT_USERNAME")
RIOT_PASSWORD = os.getenv("RIOT_PASSWORD")
USER_REGION = os.getenv("USER_REGION")
CLIENT_IP = socket.gethostbyname(hostname)

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
    COOKIES = getCookies()

    credentials = {
        'type': 'auth',
        'username': RIOT_USERNAME,
        'password': RIOT_PASSWORD
    }
    headers = {
        'X-Forwarded-For': f'{CLIENT_IP}'
    }
    response = requests.put(AUTHORIZATION, headers=headers, json=credentials, cookies=COOKIES)

    # WHAT IF WRONG USERNAME AND PASSWORD -> FIXING....

    uri = response.json()['response']['parameters']['uri']
    access_token = urllib.parse.parse_qs(uri)
    access_token = access_token['https://playvalorant.com/#access_token'][0]

    return access_token


def getEntitlementToken():
    ACCESS_TOKEN = getAccessToken()
    COOKIES = getCookies()

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
    }
    response = requests.post(ENTITLEMENT_TOKEN_LINK, headers=headers, json={}, cookies=COOKIES)
    entitlement_token = response.json()['entitlements_token']

    res = make_response('adding entitlement_token cookie')
    res.set_cookie('entitlement_token', entitlement_token)

    return entitlement_token


def user():
    ACCESS_TOKEN = getAccessToken()
    COOKIES = getCookies()

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'X-Forwarded-For': f'{CLIENT_IP}'
    }

    response = requests.post(AUTHORIZATION_INFORMATION, headers=headers, json={}, cookies=COOKIES)
    data = response.json()
    user_id = data['sub']
    riot = data['acct']['game_name']
    tagline = data['acct']['tag_line']
    game_name = "{0} #{1}".format(riot, tagline)

    return user_id, game_name


def getMatchHistory():
    PLAYER_ID, IGN = user()
    ACCESS_TOKEN = getAccessToken()
    ENTITLEMENT_TOKEN = getEntitlementToken()
    COOKIES = getCookies()
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'X-Riot-Entitlements-JWT': f'{ENTITLEMENT_TOKEN}',
        'X-Riot-ClientPlatform': CLIENT_PLATFORM,
    }

    MATCH_LINK = f'https://pd.{USER_REGION}.a.pvp.net/mmr/v1/players/{PLAYER_ID}/competitiveupdates?startIndex=0&endIndex=1'

    response = requests.get(MATCH_LINK, headers=headers, cookies=COOKIES)

    data = response.json()['Matches'][0]

    tier_after_update = data['TierAfterUpdate']
    tier_before_update = data['TierBeforeUpdate']
    ranked_rating_earned = data['RankedRatingEarned']

    return tier_after_update, tier_before_update, ranked_rating_earned, IGN


@app.route('/')
def start():
    print(getMatchHistory())
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
