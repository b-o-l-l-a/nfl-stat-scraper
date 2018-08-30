# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 11:13:17 2017

@author: greg.bolla
"""

import requests
from bs4 import BeautifulSoup
import re
import sys

sys.path.insert(0, "C:\\Users\\greg.bolla\\Desktop\\Personal\\Football Spreads\\updated_scripts")
import weekly_positional_stats
import yearly_positional_stats
import player_stats_utils

def get_indiv_player_stats(tr, position_dict, starter_dict, starter_counter, team, detail_link, base_url, year, week, ranges_dict, week_ranges_list, team_abbr_dict, team_game_num, upcoming = False):
   
    if upcoming == False:
        player = tr.th.string
        player_link = tr.a['href']
        player_url = base_url + player_link
        position = tr.td.string.strip()   
    else:
        player = tr["player_name"]
        position = tr["position"]
        if str(tr["player_link"]) == 'nan':
            player_link = str(tr["url"])
        else:
            player_link = str(tr["player_link"])
            
        player_url = base_url + str(player_link)      
    

    try:        
        standardized_pos = [k for k, v in position_dict.iteritems() if position in v["eligible_positions"]][0]
    except IndexError:
        print("position {} not found in position_dict".format(position))

    print("{} / {} / {}".format(player, standardized_pos, player_link))  
    sys.stdout.flush()
    
    if not standardized_pos in starter_counter:
        starter_counter[standardized_pos] = 1
        starter_dict[standardized_pos] = {"players":[]}
    else:
        starter_counter[standardized_pos] += 1

    player_dict = {
        "name" : str(player),
        "player_link" : player_link,
        "stats" : {}
    }

    if str(player_link) != 'nan':    
        player_html = requests.get(player_url, verify=False).content
        player_soup = BeautifulSoup(re.sub("<!--|-->","", player_html), "lxml")      
    else:
        player_html = None
        player_soup = None
        
    if standardized_pos != "QB":
        tbl_id = player_stats_utils.get_final_tbl_id(standardized_pos, player_soup)
        final_tbl_id_list = [tbl_id]
    else: # want passing and rushing stats for QBS
        final_tbl_id_list = ["passing", "rushing_and_receiving"]
        
    #side = position_dict[standardized_pos]["primary_side"]
    for final_tbl_id in final_tbl_id_list:
        try:
            player_stats = player_soup.find(id=final_tbl_id).tbody
            player_stat_rows = player_stats.findAll('tr')
        except AttributeError:
            player_stats = None            
            player_stat_rows = []
            
        team_abbr = team_abbr_dict.keys()[team_abbr_dict.values().index(team)]   
        yrs_w_team, yrs_career, age = player_stats_utils.get_yrs_experience(player_stat_rows, year, team_abbr)
        player_dict['stats'].update({
            'yrs_w_team' : yrs_w_team,
            'yrs_career' : yrs_career,
            'age'        : age
        })
                
        yearly_positional_stats_dict = yearly_positional_stats.get_yearly_positional_stats(player_stats, ranges_dict, standardized_pos, final_tbl_id, year, position_dict)
        player_dict['stats'].update(yearly_positional_stats_dict)
    
    weekly_positional_stats_dict = weekly_positional_stats.get_weekly_player_stats(base_url, position_dict, player_link, year, detail_link, week, week_ranges_list, standardized_pos, upcoming, team_game_num) 
    player_dict['stats'].update(weekly_positional_stats_dict)
    
    return player_dict, standardized_pos, starter_counter
