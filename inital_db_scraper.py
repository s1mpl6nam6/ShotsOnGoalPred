from bs4 import BeautifulSoup
import requests
import argparse
from datetime import date
import re

# premier league site: https://www.premierleague.com/en/matches?competition=8&season=2025&matchweek=11&month=11
# vpn rotations: https://gist.github.com/Lazza/bbc15561b65c16db8ca8

# ? seems to get match story: https://blazesdk-prod-cdn.clipro.tv/api/blazesdk/v1.3/stories?ApiKey=b95c92c4952a43a5bc5f7e692c1e3636&clientPlatform=Web&labelsFilterExpression=%5Band%2C+single_match_page_stories%2C++g_2561981%5D&labelsPriority=%5B%5D


def main(args):

    #https://www.espn.com/soccer/scoreboard/_/date/20231119/league/eng.1
    #                                              2023/11/19 <-- is the date
    url_suffix = "https://www.espn.com/soccer/scoreboard/_/date/"
    url_prefix = "/league/eng.1"

    current_date = date.today()
    current_date = current_date.replace("", )
    print(current_date)


    headers = requests.utils.default_headers()
    headers.update({
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0",
    })
    if args.fetch != 0:
        try:
            response = requests.get(url, headers=headers, allow_redirects=False)
            response.raise_for_status()
            html_content = response.text
        except requests.exceptions.RequestException as e:
            print("ERROR FETCHING URL: \n", e)
            exit()
        with open("html_page_content.txt", 'w') as file:
            file.write(html_content)
    else: 
        with open("html_page_content.txt", 'r') as file:
            html_content = file.read()
    
    if len(html_content) < 1:
        print("Please fetch HTML from server: 'python intitial_db_scraper.py 1'")
        exit()

    soup = BeautifulSoup(html_content, 'html.parser')

    date_carousel_list = soup.find_all(class_ = "DatePicker DatePicker--5DayMobile")
    if len(date_carousel_list) > 1:
        print("More than one Date carousel")
    else:
        date_carousel_div = date_carousel_list[0]
        print(date_carousel_div.prettify())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fetch", type=int, default=0)
    args = parser.parse_args()
    main(args)
