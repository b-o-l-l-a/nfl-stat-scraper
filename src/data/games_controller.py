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

def get_games_stats(config, upcoming_flg, begin_yr = None, begin_wk = None):
    
    if upcoming_flg:
        start_yr = datetime.datetime.now().year
        current_yr = datetime.datetime.now().year + 1
    else:
        start_yr = config["start_yr"] if begin_yr is None else begin_yr
        current_yr = datetime.datetime.now().year

    root_dir = os.getcwd().replace("/src", "").replace("/data", "")
    data_dir = os.path.join(root_dir, "data", "external")
    games_by_team_path = os.path.join(data_dir, "game_summary_by_team.csv")
    
    for season in range(start_yr, current_yr):
        season = Season(season, config)
        games_table = season.get_schedule_table()
        weekly_dict = season.get_weekly_dict(games_table, upcoming_flg, begin_yr, begin_wk)
        
        for week_num, games in weekly_dict.items():
            
            week = Week(season, week_num, weekly_dict[str(week_num)], upcoming_flg)    
            
            print("\nYear: {} / Week: {}".format(season.season, week_num))
            for game_idx, game_info in enumerate(week.games):
                if os.path.exists(games_by_team_path):
                    games_by_team_df = pd.read_csv(games_by_team_path)
                else: games_by_team_df = pd.DataFrame()
                
                game = Game(week, week.games[game_idx], upcoming_flg)
                print(game.game_full_url)

                for team_idx, team_info in enumerate(game.teams_list):

                    opp_info = game.teams_list[abs(team_idx - 1)]
                    home_flg = team_info["home_flg"]
                    team = Team(game, team_info["team"], opp_info["team"], home_flg)
                    opponent = Team(game, opp_info["team"], team_info["team"], opp_info["home_flg"])
                    team_row_dict = team.get_team_game_summary(game)
                    team_game_stats_dict = team.get_indiv_game_stats()
                    rush_dir_dict = team.get_rush_dir_stats()
                    drive_summary_dict = team.get_drive_summary_dict()

                    team_row_dict.update(team_game_stats_dict)
                    team_row_dict.update(rush_dir_dict)
                    team_row_dict.update(drive_summary_dict)

                    team_snap_rows = team.get_game_snap_rows(opp_flg = False)            
                    team_game_player_stats = get_player_stats_rows(team_snap_rows, team)
                                                
                    opp_snap_rows = team.get_game_snap_rows(opp_flg = True)            
                    opp_game_player_stats = get_player_stats_rows(opp_snap_rows, opponent)
                        
                    team_game_player_df = pd.DataFrame(team_game_player_stats)
                    team.drop_to_csv(team_game_player_df, "game_summary_by_player")
                    
                    opp_game_player_df = pd.DataFrame(opp_game_player_stats)
                    
                    if len(team_game_player_df) > 0 and len(opp_game_player_df) > 0:
                        team_pos_dict = team.aggregate_game_stats_by_pos(\
                             team_game_player_df, opp_flg = False, \
                             off_snaps = team_row_dict["team_plays"], def_snaps = team_row_dict["opp_plays"])
                        opp_pos_dict = team.aggregate_game_stats_by_pos(\
                             opp_game_player_df, opp_flg = True, \
                             off_snaps = team_row_dict["opp_plays"], def_snaps = team_row_dict["team_plays"])
                    
                        team_row_dict.update(team_pos_dict)
                        team_row_dict.update(opp_pos_dict)
                    team_idx_dict = team.get_idx_cols(games_by_team_df, team_row_dict)
                    team_row_dict.update(team_idx_dict)
                    
                    team.add_row_to_csv(team_row_dict)

def get_player_stats_rows(snap_rows, team):
    game_player_stats = []
    for tr in snap_rows:
        player_name = tr.th.a.string if tr.th.a is not None else None
        if player_name is None:
            continue

        player_link = tr.th.a['href']
        position = tr.find("td", {"data-stat" : "pos"}).string
        player_game = Player(player_name, player_link, team, position)

        player_stats_dict = player_game.get_player_summary()
        num_snaps, perc_snaps = player_game.get_snaps(tr)
        player_stats_dict["perc_snaps"] = float(perc_snaps)
        player_stats_dict["snaps"] = float(num_snaps)

        pos_stats_flg = player_game.get_pos_stats_flg(tr)
        if pos_stats_flg == True:

            positional_player = player_game.player_class(player_game)
            pos_player_stats = positional_player.get_positional_stats(player_game)
            player_stats_dict.update(pos_player_stats)
        game_player_stats.append(player_stats_dict)
    
    return game_player_stats
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
    
    get_games_stats(config, args.upcoming, args.year, args.week)
    