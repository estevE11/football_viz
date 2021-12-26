import requests
import json
import time

f = open("API_KEY", "r")
API_KEY = f.read()

BASE_URL = "https://api.football-data.org/v2/"


def req(filters):
    r = requests.get(BASE_URL + filters,   headers={'X-Auth-Token': API_KEY})
    return json.loads(r.content)

def request_and_save_match_day(season, league, md):
    res = {}
    while True:
        filters = "competitions/" + league.upper() + "/matches/?matchday=" + str(md) + "&season=" + str(season)
        res = req(filters)
        if "errorCode" not in res:
            break
        elif res.errorCode == 429:
            time.sleep(60)


    f = open("store/" + league + "/" + str(season) + "/md_" + str(md) + ".json", "w")
    f.write(json.dumps(res))
    f.close()

    request_and_save_match_day(2021, "pd", 19)