from team_stats.scrape_game_results import scrape_yearly_games

import warnings
import os

def game_stats_controller():

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        games_df = scrape_yearly_games()



if __name__ == "__main__":
    game_stats_controller()