import datetime
import json
import os
import socket
import sys
import time
import urllib

import requests
from dotenv import load_dotenv, find_dotenv
from flask import Flask, Response, render_template, make_response, session, request, url_for
from flask_fontawesome import FontAwesome

from helpers.mapNames import mapNames
from helpers.rankNames import rankNames

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
fa = FontAwesome(app)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(seconds=3600)


def getCookies():
    if session.get('riot_cookies'):
        return session.get('riot_cookies')

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
    print("getCookies", response)
    cookies = response.cookies
    session['riot_cookies'] = cookies.get_dict()

    return cookies


def getAccessToken():
    if session.get('riot_access_token'):
        return session.get('riot_access_token')

    COOKIES = session.get('riot_cookies')
    if not COOKIES:
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
    print("getAccessToken", response)
    uri = response.json()['response']['parameters']['uri']
    data = urllib.parse.parse_qs(uri)

    access_token = data['https://playvalorant.com/#access_token'][0]
    expires_in = data['expires_in'][0]

    session['riot_access_token'] = access_token
    session['riot_access_token_expires_in'] = expires_in

    return access_token


def getEntitlementToken():
    if session.get('riot_entitlement_token'):
        return session.get('riot_entitlement_token')

    ACCESS_TOKEN = session.get('riot_access_token') if session.get('riot_access_token') else getAccessToken()
    COOKIES = session.get('riot_cookies') if session.get('riot_cookies') else getCookies()

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
    }

    response = requests.post(ENTITLEMENT_TOKEN_LINK, headers=headers, json={}, cookies=COOKIES)
    entitlement_token = response.json()['entitlements_token']
    print("getEntitlementToken", response)
    session['riot_entitlement_token'] = entitlement_token

    return entitlement_token


def user():
    player_id, game_name = session.get('riot_player_id'), session.get('riot_game_name')

    if player_id and game_name:
        return player_id, game_name

    ACCESS_TOKEN = session.get('riot_access_token') if session.get('riot_access_token') else getAccessToken()
    COOKIES = session.get('riot_cookies') if session.get('riot_cookies') else getCookies()

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'X-Forwarded-For': f'{CLIENT_IP}'
    }

    response = requests.post(AUTHORIZATION_INFORMATION, headers=headers, json={}, cookies=COOKIES)
    print("user", response)
    data = response.json()

    player_id = data['sub']
    riot = data['acct']['game_name']
    tagline = data['acct']['tag_line']
    game_name = "{0} #{1}".format(riot, tagline)

    session['riot_player_id'] = player_id
    session['riot_game_name'] = game_name

    return player_id, game_name


def sessionCheck():
    PLAYER_ID, IGN = user()

    if not PLAYER_ID and not IGN:
        PLAYER_ID, IGN = user()

    ACCESS_TOKEN = session.get('riot_access_token') if session.get('riot_access_token') else getAccessToken()
    ENTITLEMENT_TOKEN = session.get('riot_entitlement_token') if session.get(
        'riot_entitlement_token') else getEntitlementToken()
    COOKIES = session.get('riot_cookies') if session.get('riot_cookies') else getCookies()

    return ACCESS_TOKEN, ENTITLEMENT_TOKEN, COOKIES, PLAYER_ID, IGN


def getFileLocation():
    try:
        file = open('api/status/rank.json', 'r+')
        path = os.path.normpath(file.name)
        file.close()
    except sys.exc_info()[0] as e:
        print('Error Message: ', e)
        return None
    return path


def updateJSON(data):
    PATH = getFileLocation()

    game_time = data['match_date'] // 1000
    match_date = time.strftime('%m-%d-%Y', time.localtime(game_time))

    with open(PATH, 'r') as ranks:
        rank = json.load(ranks)

    rank["statistics"] = {
        "tier_after_update": data['tier_after_update'],
        "tier_before_update": data['tier_before_update'],
        "ranked_rating_earned": data['ranked_rating_earned'],
        "ranked_ratingAfter_update": data['ranked_ratingAfter_update'],
        "competitive_map": data['competitive_map'],
        "match_date": match_date,
        "ign": data['ign']
    }
    with open(PATH, 'w') as fp:
        json.dump(rank, fp, indent=2)

    data['match_date'] = match_date

    return data


def getRankJSON():
    PATH = getFileLocation()

    with open(PATH, 'r') as ranks:
        rank = json.load(ranks)

    data = {
        "tier_after_update": rank['statistics']['tier_after_update'],
        "tier_before_update": rank['statistics']['tier_before_update'],
        "ranked_ratingAfter_update": rank['statistics']['ranked_ratingAfter_update'],
        "ranked_rating_earned": rank['statistics']['ranked_rating_earned'],
        "competitive_map": rank['statistics']['competitive_map'],
        "match_date": rank['statistics']['match_date'],
        "ign": rank['statistics']['ign'],
    }

    return data


def rankStatus(rank):
    if rank < 0:
        return "fas fa-chevron-circle-down"
    return "fas fa-chevron-circle-up"


def getMatchHistory():
    ACCESS_TOKEN, ENTITLEMENT_TOKEN, COOKIES, PLAYER_ID, IGN = sessionCheck()

    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'X-Riot-Entitlements-JWT': f'{ENTITLEMENT_TOKEN}',
        'X-Riot-ClientPlatform': CLIENT_PLATFORM,
    }

    MATCH_LINK = f'https://pd.{USER_REGION}.a.pvp.net/mmr/v1/players/{PLAYER_ID}/competitiveupdates?startIndex=0&endIndex=1'

    response = requests.get(MATCH_LINK, headers=headers, cookies=COOKIES)
    if not response.status_code == '200':
        defaultRank = getRankJSON()
        return defaultRank

    data = response.json()['Matches'][0]
    rank_info = {
        "tier_after_update": data['TierAfterUpdate'],
        "tier_before_update": data['TierBeforeUpdate'],
        "ranked_rating_earned": data['RankedRatingEarned'],
        "ranked_ratingAfter_update": data['RankedRatingAfterUpdate'],
        "competitive_map": mapNames(data['MapID']),
        "match_date": data['MatchStartTime'],
        "ign": IGN
    }

    if not rank_info['tier_after_update'] == 0:
        updatedRank = updateJSON(rank_info)
        return updatedRank

    defaultRank = getRankJSON()
    return defaultRank


@app.route('/')
def start():
    stats = getMatchHistory()

    currentRankName = rankNames(stats['tier_after_update'])
    pastRank = rankNames(stats['tier_before_update'])

    data = {
        "currentRankName": currentRankName[0],
        "progressBarColor": currentRankName[1],
        "currentColor": currentRankName[2],
        "currentRankCode": str(stats['tier_after_update']),
        "pastRank": pastRank[0],
        "rankProgression": stats['ranked_ratingAfter_update'],
        "rankPoints": stats['ranked_rating_earned'],
        "rankPointsStatus": rankStatus(stats['ranked_rating_earned']),
        "map": stats['competitive_map'],
        "match_date": stats['match_date'],
        "name": stats['ign']
    }
    print(data)
    return render_template("valorantRank.html.j2", **data)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    data = start()

    response = Response(data, mimetype="image/svg+xml")
    response.headers["Cache-Control"] = "s-maxage=1"

    return response


if __name__ == '__main__':
    app.secret_key = 'VALORANT_RIOT_GAMES'
    app.run(debug=True)
