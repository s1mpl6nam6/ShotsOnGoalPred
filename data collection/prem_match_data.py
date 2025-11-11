import requests
import json
import pandas as pd

headers = requests.utils.default_headers()
headers.update({
    "Origin": "https://www.premierleague.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0",
})

# https://sdp-prem-prod.premier-league-prod.pulselive.com/api/v2/matches?competition=8&season=2025&matchweek=12&_limit=100
# ^^ gets matches list

# ? this should be stat page: https://sdp-prem-prod.premier-league-prod.pulselive.com/api/v3/matches/2561981/stats


def main():
    count = 0
    final_dataset = []
    years = [2019, 2020, 2021, 2022, 2023, 2024, 2025]
    for year in years:
        for week in range(38):
            data = get_fetch_url(year, week)
            if data == "error":
                continue
            for match_ in data:
                shots_on = get_shots_on_target(match_["match_id"])
                # TODO if match is in future, dont call function  
                if shots_on == "error":
                    continue
                for stat in shots_on:
                    match_[stat["side"] + "_shots_on_target"] = stat["shots_on_target"]
                final_dataset.append(match_)
                count += 1
            if count % 50 == 0:
                print(f"{count} matches processed, year: {year}, week: {week}")
    df = pd.DataFrame(final_dataset)
    df.to_csv("shots_per_match.csv", index=False)
            


def get_fetch_url(season, matchweek):
    url = f"https://sdp-prem-prod.premier-league-prod.pulselive.com/api/v2/matches?competition=8&season={season}&matchweek={matchweek}&_limit=100"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()["data"]
    except requests.exceptions.RequestException as e:
        print("ERROR FETCHING URL: \n", e)
        return "error"
    
    res = []
    for entry in data:
        res.append({"match_id" : entry["matchId"], "away_team_name" : entry["awayTeam"]["name"], "home_team_name" : entry["homeTeam"]["name"], "datetime": entry["kickoff"]})
    return res


def get_shots_on_target(match_id):
    url = f"https://sdp-prem-prod.premier-league-prod.pulselive.com/api/v3/matches/{match_id}/stats"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("ERROR FETCHING URL: \n", e)
        return "error"
    if len(data) < 1:
        return [
                {"side" : "Away", "shots_on_target" : "N/A"},
                {"side" : "Home", "shots_on_target" : "N/A"}
            ]
    
    res = []
    for team in data:
        try: 
            attempts = team["stats"]["ontargetScoringAtt"]
        except KeyError as e:
            attempts = 0
        res.append({"side" : team["side"], "shots_on_target" : attempts})
    return res


if __name__ == "__main__":
    main()