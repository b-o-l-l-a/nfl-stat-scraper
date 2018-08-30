# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 11:11:43 2017

@author: greg.bolla
"""

import sys
sys.path.insert(0, "C:\\Users\\greg.bolla\\Desktop\\Personal\\Football Spreads\\updated_scripts")
import player_stats_utils

def get_yearly_positional_stats(player_stats, ranges_dict, standardized_pos, final_tbl_id, year, position_dict):
        
    positional_stat_row = {}
    stat_calc_dict = player_stats_utils.get_stat_calc()
    
    if standardized_pos == "QB":
        if final_tbl_id in ["rushing_and_receiving", "receiving_and_rushing"]:
            stats_to_add = position_dict["QB"]["rushing_scraped_stats"]
        elif final_tbl_id == "passing":
            stats_to_add = position_dict["QB"]["passing_scraped_stats"]
    else:
        stats_to_add = position_dict[standardized_pos]["scraped_stats"]
    
    
    for k, v in ranges_dict.iteritems():
        added_stats_dict = {
            "pro_bowls": 0,
            "all_pros" : 0
        }
        
        for added_stat in stats_to_add:
            added_stats_dict[added_stat] = 0
            
        try:
            range_start = eval(v)    
        except AttributeError:
            print("in AttributeError except for range start, going to string without a tag")
            try:
                range_start = eval("int(player_stats.find('th', {'data-stat' : 'year_id'}).string)")       
            except AttributeError:
                range_start = year
        
        for yr in range(range_start, year):    
        
            try: 
                yr_row = player_stats.find('a',text=str(yr)).parent.parent
            except AttributeError:
                try:
                    yr_row = player_stats.find('th', text=str(yr)).parent
                except AttributeError:
                    yr_row = None
                    next
            if yr_row is not None:
                added_stats_dict["pro_bowls"], added_stats_dict["all_pros"] = player_stats_utils.get_all_pro_and_pro_bowls(yr_row, added_stats_dict["pro_bowls"], added_stats_dict["all_pros"])   
                
                for stat_k, stat_v in added_stats_dict.iteritems():
                    if stat_k not in ["pro_bowls", "all_pros"]:
                        try:
                            added_stats_dict[stat_k] += eval(stat_calc_dict[stat_k])
                        except:                            
                            #print("in exception for {k} / {standardized_pos} / {stat_k}".format(**locals()))
                            pass
        
        for added_stat_name, added_stat_val in added_stats_dict.iteritems():
            positional_stat_row["{}_{}".format(k, added_stat_name)] = added_stat_val
                   
    return positional_stat_row
    