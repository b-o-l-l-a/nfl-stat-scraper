# -*- coding: utf-8 -*-
"""
Created on Fri Sep 08 20:30:29 2017

@author: greg.bolla
"""
import warnings
import pandas as pd
from bs4 import BeautifulSoup
import sys
import requests
import re
import time

sys.path.insert(0, "C:\\Users\\greg.bolla\\Desktop\\Personal\\Football Spreads\\updated_scripts")
import utils
#import player_stats_utils
import indiv_player_stats
import aggregate_starter_stats

def get_player_predictors(redo_list, week_to_pred, current_yr, upcoming = False):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        current_yr = int(current_yr)
        team_abbr_dict = utils.get_full_team_names()
        
        position_dict = utils.get_position_dict()
        base_url = ""
        
        full_ranges_dict = {
            "prevyear" : "year - 1",
            "twoyear"  : "year - 2",
            "threeyr"  : "year - 3",
            "career"    : "int(player_stats.find('th', {'data-stat' : 'year_id'}).a.string)"
        }
        
        week_ranges_list = [2, 4, 6]
        full_ranges_list = [k for k, v in full_ranges_dict.iteritems()] 
        full_ranges_list.extend(["prev{}wks".format(elem) for elem in week_ranges_list])
        
        if upcoming == True:
            print('starting indiv players')
            games_csv = pd.read_csv("C:\\Users\\greg.bolla\\Desktop\\Personal\\Football Spreads\\game_results_w_lines.csv")
            games_csv = games_csv[games_csv["year"].astype(int) == current_yr]
            games_csv = games_csv[games_csv["week"].astype(int) == week_to_pred]      
            print(games_csv.head())
            all_starters = pd.read_csv("C:\\Users\\greg.bolla\\Desktop\\Personal\\Football Spreads\\new_player_stats\\upcoming\\weekly_starters.csv")
            weekly_starters = all_starters[all_starters["week"] == week_to_pred]            
            #active_players = get_active_players()
            active_players = pd.read_csv("C:\\Users\\greg.bolla\\Desktop\\Personal\\Football Spreads\\new_player_stats\\upcoming\\active_players.csv")        
        else:
            games_csv = pd.read_csv("C:\\Users\\greg.bolla\\Desktop\\Personal\\Football Spreads\\game_results_w_lines.csv")

        if redo_list:
            games_csv = games_csv[games_csv["detail_link"].isin(redo_list)]            
        
        output_player_predictor_df = pd.DataFrame()   
        
        for index, row in games_csv.iterrows():
            #try:
                year = int(row['year'])
                week = row['week']
                url_suffix = row['detail_link']
                url = base_url + url_suffix    
                home_team = row['home']
                away_team = row['away']
                favorite = row['favorite']
                print("Year {} / Week {} / {} at {} / link: {}".format(year, week, away_team, home_team, url_suffix))
                sys.stdout.flush()

                html = requests.get(url, verify=False).content
                soup = BeautifulSoup(re.sub("<!--|-->","", html), "lxml")  
                
                if upcoming == True: 
                    vis_starters = weekly_starters[weekly_starters["team"] == away_team].merge(active_players, on='player_name', how='left')
                    vis_starters = vis_starters.drop_duplicates(subset='player_name')                    
                    vis_starters_rows = []                 
                    for index, tr in vis_starters.iterrows():
                        vis_starters_rows.append(tr)
                                                            
                    home_starters = weekly_starters[weekly_starters["team"] == home_team].merge(active_players, on='player_name', how='left')
                    home_starters = home_starters.drop_duplicates(subset='player_name')                   
                    home_starters_rows = []                    
                    for index, tr in home_starters.iterrows():
                        home_starters_rows.append(tr)
                        
                else:    
                    home_starters = soup.find(id="home_starters").tbody
                    home_starters_rows = home_starters.findAll('tr')
                    
                    vis_starters = soup.find(id="vis_starters").tbody
                    vis_starters_rows = vis_starters.findAll('tr')
                
                home_starter_counter = {}
                away_starter_counter = {}
                
                home_starter_dict = {}
                away_starter_dict = {}
                
                if upcoming == True:
                    home_team_game_num = utils.get_current_game(base_url, year, home_team)
                    print("{home_team} game number: {home_team_game_num}".format(**locals()))
                    away_team_game_num = utils.get_current_game(base_url, year, away_team)
                    print("{away_team} game number: {away_team_game_num}".format(**locals()))
                else:
                    home_team_game_num = None
                    away_team_game_num = None
                    
                for tr in home_starters_rows:    
                    player_dict, standardized_pos, home_starter_counter = indiv_player_stats.get_indiv_player_stats(tr, position_dict, home_starter_dict, home_starter_counter, home_team, url_suffix, base_url, year, week, full_ranges_dict, week_ranges_list, team_abbr_dict, home_team_game_num, upcoming)                                      
                    home_starter_dict[standardized_pos]["players"].append(player_dict) 
                    time.sleep(6)
                
                for tr in vis_starters_rows:                   
                    player_dict, standardized_pos, away_starter_counter = indiv_player_stats.get_indiv_player_stats(tr, position_dict, away_starter_dict, away_starter_counter, away_team, url_suffix, base_url, year, week, full_ranges_dict, week_ranges_list, team_abbr_dict, away_team_game_num, upcoming)                   
                    away_starter_dict[standardized_pos]["players"].append(player_dict)                                        
                    time.sleep(6)
                
                if home_team == favorite:
                    home_side = "fave"
                    away_side = "dog"
                    home_favorite = True
                elif away_team == favorite: 
                    home_side = "dog"
                    away_side = "fave"
                    home_favorite = False
                else:
                    home_side = None
                    away_side = None
                    print("No favorite in game: {}".format(row['detail_link']))     
                    
                aggregated_home_starter_stats = aggregate_starter_stats.get_aggregate_starter_stats(home_starter_dict, full_ranges_list, home_side, position_dict)
                aggregated_away_starter_stats = aggregate_starter_stats.get_aggregate_starter_stats(away_starter_dict, full_ranges_list, away_side, position_dict)

                predictor_row_dict = {}
                predictor_row_dict['detail_link'] = row['detail_link']
                predictor_row_dict['home_favorite'] = home_favorite
                predictor_row_dict['year'] = year
                predictor_row_dict['week'] = week
                if home_favorite == True:
                    predictor_row_dict['favorite'] = home_team
                    predictor_row_dict['underdog'] = away_team
                elif home_favorite == False:
                    predictor_row_dict['underdog'] = home_team
                    predictor_row_dict['favorite'] = away_team        
                
                pos_predictors = dict(aggregated_home_starter_stats, **aggregated_away_starter_stats)
                predictor_row_dict.update(pos_predictors)
                predictor_row_df = pd.DataFrame(data = predictor_row_dict, index=[0])                
                output_player_predictor_df = output_player_predictor_df.append(predictor_row_df)                
                #predictor_row_df.to_csv("C:\\Users\\greg.bolla\\Desktop\\Personal\\Football Spreads\\new_player_stats\\upcoming\\full_predictors\\Week {week_to_pred}\\week{week_to_pred}_player_predictors_{index}.csv".format(**locals()))
                
                
            #except Exception as e:
            #    print(e)
            #    print("couldn't add data for game")
            #    time.sleep(60)
            #    continue
        
        if upcoming == True:
            output_path = "C:\\Users\\greg.bolla\\Desktop\\Personal\\Football Spreads\\new_player_stats\\upcoming\\full_predictors\\Week {week_to_pred}\\week{week_to_pred}_player_predictors.csv".format(**locals())
        else:
            output_path = "C:\\Users\\greg.bolla\\Desktop\\Personal\\Football Spreads\\new_player_stats\\player_predictors.csv"
            
        output_player_predictor_df.to_csv(output_path)
        #return output_player_predictor_df
        
if __name__ == "__main__":
    
    print("starting get_player_predictions")
    redo_list = None
    get_player_predictors(redo_list, week_to_pred = 6, current_yr = 2017, upcoming = True)
