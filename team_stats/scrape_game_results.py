import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import utils
import re
import time
import warnings

def scrape_yearly_games():
    
    year_url_base_string = "years/{}/games.htm"
    path = os.getcwd()

    config_dict = utils.get_config(path)
    print(config_dict)

    base_url = config_dict["base_url"]
    start_yr = config_dict["start_yr"]
    current_yr = config_dict["current_yr"]
    wait_time = config_dict["wait_time"]

    game_results_cols = [
        "year",
        "week_num",
        "game_date",
        "game_link",
        "home_winner",
        "winner",
        "pts_win",
        "loser",
        "pts_lose"
    ]
    output_df = pd.DataFrame(columns = game_results_cols)
    for yr in range(start_yr, current_yr):
    #for yr in range(start_yr, start_yr + 1):    
        yearly_games_url = base_url + year_url_base_string.format(yr)
        print(" --- accessing {yr} games at URL : {yearly_games_url}".format(**locals()))

        yr_gamelog_html = requests.get(yearly_games_url, verify=False).content
        yr_gamelog_html = yr_gamelog_html.decode("utf-8")
        yr_gamelog_soup = BeautifulSoup(re.sub("<!--|-->","", yr_gamelog_html), "lxml") 
        #print(yr_gamelog_html)
        # find <table/> id ="games"

        games_table = yr_gamelog_soup.find(id="games")
        games_rows = games_table.findAll('tr')

        for game in games_rows:

            append_flg = check_row_validity(game)    
            if append_flg == False:
                continue

            game_dict = {}        
            game_cols = game.findAll('td')
            game_dict["year"] = yr
            game_dict["week_num"] = game.findAll("th", {"data-stat" : "week_num"})[0].string
           
            for td in game_cols:
                data_stat = td.get('data-stat')
                game_dict = clean_stat(game_dict, td, data_stat)

            output_df = output_df.append(game_dict, ignore_index = True)

        time.sleep(wait_time)

    csv_drop_path = os.getcwd() + "/output/step_1_game_results.csv"
    print("dropping CSV to {}".format(csv_drop_path))
    output_df.to_csv(csv_drop_path, index = False)

    return output_df
def clean_stat(game_dict, td, data_stat):
    if data_stat in ["game_date", "pts_lose"]:
        game_dict[data_stat] = td.string
    if data_stat in ["winner", "loser"]:
        game_dict[data_stat] = td.a.string
    if data_stat == "game_location":
        if td.string == "@":
            game_dict["home_winner"] = False
        else:
            game_dict["home_winner"] = True
    if data_stat == "pts_win":
        game_dict[data_stat] = td.strong.string
    if data_stat == "boxscore_word":
        game_dict["game_link"] = td.a["href"]


    return game_dict

def check_row_validity(game):

    row_data = game.findAll('td')
    append_flg = True
    if len(row_data) == 0:
        append_flg =  False
    
    for td in row_data:
        data_stat = td.get('data-stat')
        if data_stat == "winner":
            if not td.find('strong'):
                append_flg =  False
    
    return append_flg