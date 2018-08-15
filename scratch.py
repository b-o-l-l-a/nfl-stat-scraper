import requests
from bs4 import BeautifulSoup
import re
import time
import warnings
import utils
import pandas as pd
import os

def scratch_get_historical_lines(historical_games_df):
    
    path = os.getcwd()
    config_dict = utils.get_config(path)

    base_url = config_dict["base_url"]
    wait_time = config_dict["wait_time"]
    game_link_col = "game_link"

    historical_games_df_cols = list(historical_games_df.columns.values)
    addtl_output_df_cols = ["weather", "favorite", "line", "over_under"]
    output_df_cols = historical_games_df_cols + addtl_output_df_cols

    output_df = pd.DataFrame(columns=output_df_cols)
    for idx, game in historical_games_df.iterrows():
        output_df_row = {}

        for col in historical_games_df_cols:
            output_df_row[col] = game[col] 

        game_link = game[game_link_col]
        #game_info
        game_boxscore_url = base_url + game_link
        print(" --- accessing game URL : {game_boxscore_url}".format(**locals()))

        gamelog_soup = utils.fetch_url_content(game_boxscore_url)

        game_info_table = gamelog_soup.find(id="game_info")
        game_info_rows = game_info_table.findAll('tr')

        winner = output_df_row["winner"]
        loser = output_df_row["loser"]

        for tr in game_info_rows:

            if not tr.find('th'):
                continue
            if tr.th.string == "Weather":
                
                output_df_row["weather"] = tr.td.string
            elif tr.th.string == "Vegas Line":


                line_string = tr.td.string

                line_string_split_len = len(line_string.split(winner))
                if line_string_split_len == 1: #underdog won
                    favorite = loser
                    line_split = line_string.split(loser)
                else: #favorite won
                    favorite = winner
                    line_split = line_string.split(winner)

                line = line_split[-1].strip()
                
                output_df_row["line"] = line
                output_df_row["favorite"] = favorite
            elif tr.th.string == "Over/Under":
                output_df_row["over_under"] = tr.td.contents[0].strip()

        
        output_df = output_df.append(output_df_row, ignore_index = True)
        csv_drop_path = os.getcwd() + "/output/step_2_game_results_w_lines.csv"
        output_df.to_csv(csv_drop_path, index = False)
        time.sleep(wait_time)
    


if __name__ == "__main__" :
    games_df = pd.read_csv(os.getcwd() + "/output/games.csv")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        scratch_get_historical_lines(games_df)