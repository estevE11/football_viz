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

def load_stored_match_day(season, league, md):
    try:
        f = open("store/" + league + "/" + str(season) +
                "/md_" + str(md) + ".json", "r")
        return json.loads(f.read())
    except OSError:
        return None

def generate_standing_history(season, league):
    res = []
    i = 1
    while True:
        data = {}
        matchday = load_stored_match_day(season, league, i)
        if matchday == None:
            break
        for match in matchday['matches']:
            t_home = 1
            t_away = 1
            if match['score']['winner'] == 'HOME_TEAM':
                t_home = 3
                t_away = 0
            elif match['score']['winner'] == 'AWAY_TEAM':
                t_home = 0
                t_away = 3
            
            g_home = match['score']['fullTime']['homeTeam']
            g_away = match['score']['fullTime']['awayTeam']

            if i == 1:
                data[match['homeTeam']['id']] = {'pts': t_home, 'gd': g_home-g_away}
                data[match['awayTeam']['id']] = {'pts': t_away, 'gd': g_away-g_home}
            else:
                print(i)
                print(res[i-2])
                curr_home_pts = res[i-2][match['homeTeam']['id']]['pts']
                curr_away_pts = res[i-2][match['awayTeam']['id']]['pts']
                curr_home_gd = res[i-2][match['homeTeam']['id']]['gd']
                curr_away_gd = res[i-2][match['awayTeam']['id']]['gd']
                
                data[match['homeTeam']['id']] = {
                    'pts': curr_home_pts + t_home,
                    'gd': curr_home_gd + g_home-g_away
                }

                data[match['awayTeam']['id']] = {
                    'pts': curr_away_pts + t_away,
                    'gd': curr_away_gd + g_away-g_home
                }
            
        i += 1
        res.append(data)
    f = open("store/" + league + "/" + str(season) + "/pts_history.json", "w")
    f.write(json.dumps(res))
    f.close()
    return res


print(generate_standing_history(2021, 'pd'))

