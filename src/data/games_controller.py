import os 
import argparse
import pandas as pd
import datetime

from classes.Season import Season 
from classes.Week import Week 
from classes.Game import Game
from classes.Team import Team
from classes.Player import Player
from utils import get_config

def get_games_stats(config, upcoming_flg, debug_yr = None, debug_wk = None):
    
    start_yr = config["start_yr"] if debug_yr is None else debug_yr
    current_yr = datetime.datetime.now().year
      
    for season in range(start_yr, current_yr):
        season = Season(season, config)
        games_table = season.get_schedule_table()
        weekly_dict = season.get_weekly_dict(games_table, debug_yr, debug_wk)
        
        for week_num, games in weekly_dict.items():
            
            week = Week(season, week_num, weekly_dict[str(week_num)], upcoming_flg)    
            
            print("\nYear: {} / Week: {}".format(season.season, week_num))
            for game_idx, game_info in enumerate(week.games):
                game = Game(week, week.games[game_idx], upcoming_flg)
                print(game.game_full_url)

                for team_idx, team_info in enumerate(game.teams_list):

                    opp_info = game.teams_list[abs(team_idx - 1)]
                    home_flg = team_info["home_flg"]
                    team = Team(game, team_info["team"], opp_info["team"], home_flg)
                    team_row_dict = team.get_team_game_summary(game)
                    team_game_stats_dict = team.get_indiv_game_stats()
                    rush_dir_dict = team.get_rush_dir_stats()
                    drive_summary_dict = team.get_drive_summary_dict()

                    team_row_dict.update(team_game_stats_dict)
                    team_row_dict.update(rush_dir_dict)
                    team_row_dict.update(drive_summary_dict)
                    team.add_row_to_csv(team_row_dict)

                    team_snap_rows = team.get_game_snap_rows()            
                    team_game_player_stats = []

                    for tr in team_snap_rows:
                        player_name = tr.th.a.string if tr.th.a is not None else None
                        if player_name is None:
                            continue
                            
                        player_link = tr.th.a['href']
                        position = tr.find("td", {"data-stat" : "pos"}).string
                        player_game = Player(player_name, player_link, team, position)
                        
                        player_stats_dict = player_game.get_player_summary()
                        num_snaps, perc_snaps = player_game.get_snaps(tr)
                        player_stats_dict["perc_snaps"] = perc_snaps
                        player_stats_dict["snaps"] = num_snaps
                        
                        pos_stats_flg = player_game.get_pos_stats_flg(tr)
                        if pos_stats_flg == True:

                            positional_player = player_game.player_class(player_game)
                            pos_player_stats = positional_player.get_positional_stats(player_game)
                            player_stats_dict.update(pos_player_stats)
                        
                        team_game_player_stats.append(player_stats_dict)

                    team_game_player_df = pd.DataFrame(team_game_player_stats)
                    team.drop_to_csv(team_game_player_df, "game_summary_by_player")
            #team_positional_stats= list(map(lambda x: team.get_positi, team_snap_rows))
    
#     for week, games in weekly_dict[0:1].items():
#         print(week)
    
if __name__ == "__main__":

    config_dir = os.getcwd()
    config = get_config(config_dir) 
    parser = argparse.ArgumentParser(description='Collect game- and player-level data for NFL')
    parser.add_argument('-u', '--upcoming', 
        action='store_true', 
        help="if specified, collect data from previous week's games")
    
    parser.add_argument('-y', '--year', 
        type=int,
        help="if specified, start at yr")
    parser.add_argument('-w', '--week', 
        help="if specified, start at wk")
    args = parser.parse_args()   
    if args.upcoming:
        get_games_stats(config, upcoming_flg = True)
    else:
        get_games_stats(config, args.upcoming, args.year, args.week)
    