# -*- coding: utf-8 -*-
"""
Created on Sat Sep 16 14:39:27 2017

@author: greg.bolla
"""
import sys
sys.path.insert(0, "C:\\Users\\greg.bolla\\Desktop\\Personal\\Football Spreads\\updated_scripts")
import player_stats_utils

def get_aggregate_starter_stats(starter_dict, ranges_list, side, position_dict):
    
    non_aggregation_list = ["catch_perc", "per_game", "per_g", "per_att", "per_catch", 
                            "pass_td_perc", "pass_int_perc", "qbr", "win_pct", 
                            "pass_comp_pct", "sacked_perc"]
    final_dict = {}

    for key, value in starter_dict.iteritems():
 
        pos_stats = {}
        agg_stats = {}
        avg_stats = {}
        starters_info = starter_dict[key]["players"]  
        num_starters = float(len(starters_info))
        pos_starter_counter = 0
            
        for player in starters_info:           
            player_stats = player["stats"]
                
            for stat_name, stat_val in player_stats.iteritems():
                if any([elem in stat_name for elem in non_aggregation_list]):
                    continue
                else:
                    if 'agg_' + stat_name not in agg_stats:
                        agg_stats['agg_' + stat_name] = player_stats[stat_name]
                    else:
                        agg_stats['agg_' + stat_name] += player_stats[stat_name]
                        
            pos_starter_counter += 1
        
        per_game_att_stats_dict = get_per_game_att_stats(agg_stats, ranges_list, key, side, position_dict)
        
        for agg_stat, agg_val in agg_stats.iteritems():
            stat_name = agg_stat.replace('agg_', 'avg_')        
            avg_stat = float(agg_val) / float(num_starters)
            avg_stats["{}_{}_{}".format(side, key, stat_name)] = avg_stat

        pos_stats["{}_{}_num_starters".format(side, key)] = num_starters
        pos_stats.update(avg_stats)  
        final_dict.update(pos_stats)         
        final_dict.update(per_game_att_stats_dict)
    return final_dict    

def get_per_game_att_stats(agg_stats, ranges_list, position, side, position_dict):

    per_game_att_dict = {}
    
    #calculated_stats_list = position_dict[position]["calculated_stats"]
    #calculated_stats_dict = player_stats_utils.get_calculated_stats_dict("agg_stats")
    
    for time_range in ranges_list:
#        for calculated_stat in calculated_stats_list:
#            if calculated_stat == "catch_perc":
#                per_game_att_dict["{side}_{pos}_{time_range}_" + calculated_stat] = eval(calculated_stats_dict[calculated_stat])

        if position == 'QB':
            agg_wins = agg_stats['agg_{}_wins'.format(time_range)]
            agg_gs = agg_stats['agg_{}_gs'.format(time_range)]
            agg_pass_comp = agg_stats['agg_{}_pass_comp'.format(time_range)]
            agg_pass_att = agg_stats['agg_{}_pass_att'.format(time_range)]
            agg_pass_tds = agg_stats['agg_{}_pass_tds'.format(time_range)]
            agg_pass_int = agg_stats['agg_{}_pass_int'.format(time_range)]
            agg_pass_yds = agg_stats['agg_{}_pass_yds'.format(time_range)]
            agg_sacked = agg_stats['agg_{}_sacked'.format(time_range)]
            per_game_att_dict["{}_{}_{}_win_pct".format(side, position, time_range)] = player_stats_utils.clean_divided_stat(agg_wins, agg_gs)
            per_game_att_dict["{}_{}_{}_pass_comp_pct".format(side, position, time_range)] = player_stats_utils.clean_divided_stat(agg_pass_comp, agg_pass_att)
            per_game_att_dict["{}_{}_{}_pass_td_perc".format(side, position, time_range)] = player_stats_utils.clean_divided_stat(agg_pass_tds, agg_pass_att)
            per_game_att_dict["{}_{}_{}_pass_int_perc".format(side, position, time_range)] = player_stats_utils.clean_divided_stat(agg_pass_int, agg_pass_att)
            per_game_att_dict["{}_{}_{}_pass_yds_per_att".format(side, position, time_range)] = player_stats_utils.clean_divided_stat(agg_pass_yds, agg_pass_att)
            per_game_att_dict["{}_{}_{}_sacked_perc".format(side, position, time_range)] = player_stats_utils.clean_divided_stat(agg_sacked, (agg_sacked + agg_pass_att))
            per_game_att_dict["{}_{}_{}_pass_adj_yds_per_att".format(side, position, time_range)] = player_stats_utils.clean_divided_stat(
                (agg_pass_yds + ( (20 * float(agg_pass_tds)) - (45 * agg_pass_int))), 
                agg_pass_att)
            
            a = player_stats_utils.calc_qbr_input((per_game_att_dict["{}_{}_{}_pass_comp_pct".format(side, position, time_range)] - .3) * 5)
            b = player_stats_utils.calc_qbr_input((per_game_att_dict["{}_{}_{}_pass_yds_per_att".format(side, position, time_range)]  - 3) * .25)
            c = player_stats_utils.calc_qbr_input(per_game_att_dict["{}_{}_{}_pass_td_perc".format(side, position, time_range)] * 20)
            d = player_stats_utils.calc_qbr_input(2.375 - (per_game_att_dict["{}_{}_{}_pass_int_perc".format(side, position, time_range)] * 25))
            
            qbr = ((a + b + c + d) / 6) * 100
            per_game_att_dict["{}_{}_{}_qbr".format(side, position, time_range)] = qbr
        
        if position in ['RB', 'WR', 'TE']:  
            agg_rush_yds = agg_stats['agg_{}_rush_yds'.format(time_range)]
            agg_rush_att = agg_stats['agg_{}_rush_att'.format(time_range)]
            agg_games = agg_stats['agg_{}_games'.format(time_range)]
            agg_rec_yds = agg_stats['agg_{}_rec_yds'.format(time_range)]
            agg_rec = agg_stats['agg_{}_rec'.format(time_range)]
            agg_targets = agg_stats['agg_{}_targets'.format(time_range)]            
            
            per_game_att_dict["{}_{}_{}_rush_yds_per_att".format(side, position, time_range)] = player_stats_utils.clean_divided_stat(agg_rush_yds, agg_rush_att)
            per_game_att_dict["{}_{}_{}_rush_yds_per_game".format(side, position, time_range)] = player_stats_utils.clean_divided_stat(agg_rush_yds, agg_games)
            per_game_att_dict["{}_{}_{}_rush_att_per_game".format(side, position, time_range)] = player_stats_utils.clean_divided_stat(agg_rush_att, agg_games)
            
            per_game_att_dict["{}_{}_{}_rec_yds_per_catch".format(side, position, time_range)] = player_stats_utils.clean_divided_stat(agg_rec_yds, agg_rec)
            per_game_att_dict["{}_{}_{}_recs_per_game".format(side, position, time_range)] = player_stats_utils.clean_divided_stat(agg_rec, agg_games)
            per_game_att_dict["{}_{}_{}_rec_yds_per_game".format(side, position, time_range)] = player_stats_utils.clean_divided_stat(agg_rec_yds, agg_games)
            per_game_att_dict["{}_{}_{}_catch_perc".format(side, position, time_range)] = player_stats_utils.clean_divided_stat(agg_rec, agg_targets)
    
    return per_game_att_dict      
#    for k, v in ranges_dict.iteritems():


