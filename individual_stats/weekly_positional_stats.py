# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 11:15:15 2017

@author: greg.bolla
"""

import requests
from bs4 import BeautifulSoup
import re
import sys

sys.path.insert(0, "C:\\Users\\greg.bolla\\Desktop\\Personal\\Football Spreads\\updated_scripts")
import player_stats_utils

def get_weekly_player_stats(base_url, position_dict, player_link, year, detail_link, week, week_ranges_list, standardized_pos, upcoming, team_game_num):
        
    stat_calc_dict = player_stats_utils.get_stat_calc()    
    gamelog_append = player_link.replace(".htm", "")

    gamelog_base_url = "{base_url}{gamelog_append}/gamelog/".format(**locals()) 
    gamelog_url = "{gamelog_base_url}{year}".format(**locals())   
    
    try:
        gamelog_html = requests.get(gamelog_url, verify=False).content
        gamelog_soup = BeautifulSoup(re.sub("<!--|-->","", gamelog_html), "lxml") 
        
        gamelog_stats = gamelog_soup.find(id="stats").tbody
        gamelog_stat_rows = gamelog_stats.findAll('tr')    
    except:       
        gamelog_html = None
        gamelog_soup = None
        
        gamelog_stats = None
        gamelog_stat_rows = []

    if upcoming == True:
        current_game = team_game_num
    else:
        for gamelog_row in gamelog_stat_rows:
            if gamelog_row.find('td', {'data-stat' : 'game_date'}).a['href'] == detail_link:
                current_game = gamelog_row.find('td', {'data-stat' : 'game_num'}).string

    week_tbl_id = "stats"
    weekly_positional_stats_dict = {}

    if standardized_pos == "QB":
        stats_to_add = position_dict["QB"]["rushing_scraped_stats"] + position_dict["QB"]["passing_scraped_stats"]
    else:
        stats_to_add = position_dict[standardized_pos]["scraped_stats"]
        if 'gs' in stats_to_add:
            stats_to_add.remove('gs')

    for prev_wks in week_ranges_list:

        added_stats_dict = {}
        
        for added_stat in stats_to_add:
            added_stats_dict[added_stat] = 0
        
        start_game = int(current_game) - int(prev_wks)
        
        prev_yr_flg = False
        if start_game <= 0:        
            
            prev_yr_flg = True
            start_game = start_game + 16
            prev_yr = year - 1
            prev_yr_gamelog_url = "{gamelog_base_url}{prev_yr}".format(**locals())
            
            try:
                prev_yr_gamelog_html = requests.get(prev_yr_gamelog_url, verify=False).content
                prev_yr_gamelog_soup = BeautifulSoup(re.sub("<!--|-->","", prev_yr_gamelog_html), "lxml") 
            except:
                prev_yr_gamelog_html = None
                prev_yr_gamelog_soup = None
            
            try:             
                prev_yr_gamelog_stats = prev_yr_gamelog_soup.find(id="stats").tbody
                prev_yr_gamelog_stat_rows = prev_yr_gamelog_stats.findAll('tr')
                
                # yr_row doesn't make sense as a var name here, but I need to change player_stats_utils reference otherwise
                for yr_row in prev_yr_gamelog_stat_rows:
                    if int(yr_row.find('td', {'data-stat' : 'game_num'}).string) >= start_game:
                        added_stats_dict["games"] += 1
                        
                        if 'gs' in added_stats_dict: 
                            if yr_row.find('td', {'data-stat' : 'gs'}).string == "*":
                                added_stats_dict["gs"] += 1
                        
                        if 'wins' in added_stats_dict:
                            if 'W' in yr_row.find('td', {'data-stat' : 'game_result'}).string:
                                added_stats_dict["wins"] += 1
                        
                        for stat_k, stat_v in added_stats_dict.iteritems():
                            if stat_k not in ["wins", "gs", "games"]:
                                try:
                                    added_stats_dict[stat_k] += eval(stat_calc_dict[stat_k])
                                except:                            
                            #print("in exception for {k} / {standardized_pos} / {stat_k}".format(**locals()))
                                    pass
                        
            except AttributeError: 
                print("no stats in prev year")                
                pass
        
        # So now we have the previous year's stats -- if applicable -- let's capture this year's
        for yr_row in gamelog_stat_rows:
            calc_row_flg = False
            
            if prev_yr_flg == True:
                if int(yr_row.find('td', {'data-stat' : 'game_num'}).string) < int(current_game): 
                    calc_row_flg = True
                else:
                    calc_row_flg = False                   
            else:
                row_game_num = int(yr_row.find('td', {'data-stat' : 'game_num'}).string)
                if row_game_num < int(current_game) and row_game_num >= start_game:
                    calc_row_flg = True
                else: 
                    calc_row_flg = False
            
            #print("***calc_row_flg = {}".format(calc_row_flg))
            #print(game)
            if calc_row_flg == True:
                added_stats_dict["games"] += 1
                
                if 'gs' in added_stats_dict:
                    if yr_row.find('td', {'data-stat' : 'gs'}).string == "*":
                        added_stats_dict["gs"] += 1
                
                if 'wins' in added_stats_dict: 
                    if 'W' in yr_row.find('td', {'data-stat' : 'game_result'}).string:
                        added_stats_dict["wins"] += 1
                
                for stat_k, stat_v in added_stats_dict.iteritems():
                    if stat_k not in ["wins", "gs", "games"]:
                        #print(stat_k)
                        #print(stat_calc_dict[stat_k])
                        #print(eval(stat_calc_dict[stat_k]))
                        #print(" {stat_k} / {added_stats_dict[stat_k]} / {eval(stat_calc_dict[stat_k])}".format(**locals()))
                        try:
                            added_stats_dict[stat_k] += eval(stat_calc_dict[stat_k])
                            #print(added_stats_dict[stat_k])
                        except:               
                            #print('in except for stat, not incrementing stats_dict')
                            pass
        
        for added_stat_name, added_stat_val in added_stats_dict.iteritems():
            weekly_positional_stats_dict["prev{}wks_{}".format(prev_wks, added_stat_name)] = added_stat_val
        

    return weekly_positional_stats_dict