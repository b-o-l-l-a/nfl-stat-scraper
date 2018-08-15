# -*- coding: utf-8 -*-
"""
Created on Fri Sep 08 20:37:09 2017

@author: greg.bolla
"""
import re
import operator
import sys
import numpy as np

sys.path.insert(0, "C:\\Users\\greg.bolla\\Desktop\\Personal\\Football Spreads\\updated_scripts")

def get_yrs_experience(player_stat_rows, year, team):
    yrs_with_team = 0
    yrs_career = 0   
    for row in player_stat_rows:
        try:  
            row_yr = row.find('a', href=re.compile(r'years'))['href'].split('/')[2]            
        except TypeError:   
            try:
                row_yr = row.find('th', attrs={'data-stat' : 'year_id'}).string.split('*')[0]
            except AttributeError:
                continue

        row_yr = int(row_yr)

        if row_yr == year:
            try:
                current_age = int(row.find('td', attrs={'data-stat' : 'age'}).string)
            except TypeError:
                print('age not listed in year row')
                
        #elif row_yr == 2016 and year == 2017:
        #    current_age = int(row.find('td', attrs={'data-stat' : 'age'}).string) + 1
            
        yrs_with_team, yrs_career = yrs_expo_helper(row_yr, row, team, yrs_with_team, yrs_career, year)
        
    try:
        current_age
    except UnboundLocalError:
        print("current_age not defined, defaulting to 22")
        current_age = 22
    
    #print("current age: {}".format(current_age))    
    return yrs_with_team, yrs_career, current_age

def yrs_expo_helper(row_yr, row, team, yrs_with_team, yrs_career, year):
    if int(row_yr) < year:    
        yrs_career += 1
        
        try:        
            if str(row.find("td", attrs={'data-stat':'team'}).string) == team:
                yrs_with_team += 1
        except AttributeError:
            print("no team found in row for row_yr {}".format(str(row_yr)))
            pass
    
    return yrs_with_team, yrs_career

def get_all_pro_and_pro_bowls(yr_row, pro_bowls, all_pros):
    
    for child in yr_row.find('th', {'data-stat' : 'year_id'}).children:
        if child.find('*') is not None and child.find('*') >= 0:
            pro_bowls += 1
        if child.find('+') is not None and child.find('+') >= 0:
            all_pros += 1  
    
    return pro_bowls, all_pros

def clean_stat(string):
    try:
        cleaned_stat = float(string)
    except TypeError:
        cleaned_stat = 0
        
    return cleaned_stat

def calc_qbr_input(var):
    if var < 0:
        var = 0
    elif var > 2.375:
        var = 2.375
    
    return var

def clean_divided_stat(numerator, denominator, return_zero = True):
    try:
        cleaned_stat = float(numerator) / float(denominator)
    except ZeroDivisionError:
        if return_zero:
            cleaned_stat = 0
        else:
            cleaned_stat = np.nan
    return cleaned_stat

def get_stat_calc():
    
    stat_calc_dict = {
        "assists" : "player_stats_utils.clean_stat(yr_row.find('td', {'data-stat' : 'tackles_assists'}).string)",
        "av" : "int(yr_row.find('td', {'data-stat' : 'av'}).string)", 
        "comebacks" : "int(yr_row.find('td', {'data-stat' : 'comebacks'}).string)",
        "def_int" : "player_stats_utils.clean_stat(yr_row.find('td', {'data-stat' : 'def_int'}).string)" ,
        "def_int_td" : "player_stats_utils.clean_stat(yr_row.find('td', {'data-stat' : 'def_int_td'}).string)",
        "def_int_yds" : "player_stats_utils.clean_stat(yr_row.find('td', {'data-stat' : 'def_int_yds'}).string)" ,
        "def_pd" :  "player_stats_utils.clean_stat(yr_row.find('td', {'data-stat' : 'pass_defended'}).string)",
        "fumbles" : "player_stats_utils.clean_stat(yr_row.find('td', {'data-stat' : 'fumbles'}).string)",
        "forced_fum": "player_stats_utils.clean_stat(yr_row.find('td', {'data-stat' : 'fumbles_forced'}).string)",
        "games" : "player_stats_utils.clean_stat(yr_row.find('td', {'data-stat' : 'g'}).string)",
        "gs" : "player_stats_utils.clean_stat(yr_row.find('td', {'data-stat' : 'gs'}).string)",
        "gwd" : "int(yr_row.find('td', {'data-stat' : 'gwd'}).string)",  
        "losses" : "int(yr_row.find('td', {'data-stat' : 'qb_rec'}).string.split('-')[1])",        
        "pass_att" : "int(yr_row.find('td', {'data-stat' : 'pass_att'}).string)",
        "pass_comp" : "int(yr_row.find('td', {'data-stat' : 'pass_cmp'}).string)",
        "pass_int" : "int(yr_row.find('td', {'data-stat' : 'pass_int'}).string)",
        "pass_tds" : "int(yr_row.find('td', {'data-stat' : 'pass_td'}).string)",
        "pass_yds" : "int(yr_row.find('td', {'data-stat' : 'pass_yds'}).string)",
        "rec" : "player_stats_utils.clean_stat(yr_row.find('td', {'data-stat' : 'rec'}).string)" ,
        "rec_tds" : "player_stats_utils.clean_stat(yr_row.find('td', {'data-stat' : 'rec_td'}).string)" ,
        "rec_yds" : "player_stats_utils.clean_stat(yr_row.find('td', {'data-stat' : 'rec_yds'}).string)" ,
        "rush_att": "player_stats_utils.clean_stat(yr_row.find('td', {'data-stat' : 'rush_att'}).string)",
        "rush_tds": "player_stats_utils.clean_stat(yr_row.find('td', {'data-stat' : 'rush_td'}).string)" ,
        "rush_yds": "player_stats_utils.clean_stat(yr_row.find('td', {'data-stat' : 'rush_yds'}).string)",
        "sacked" : "int(yr_row.find('td', {'data-stat' : 'pass_sacked'}).string)",
        "sacks" : "player_stats_utils.clean_stat(yr_row.find('td', {'data-stat' : 'sacks'}).string)",
        "tackles" : "player_stats_utils.clean_stat(yr_row.find('td', {'data-stat' : 'tackles_solo'}).string)",            
        "targets" : "player_stats_utils.clean_stat(yr_row.find('td', {'data-stat' : 'targets'}).string)",     
        "wins" : "int(yr_row.find('td', {'data-stat' : 'qb_rec'}).string.split('-')[0])",   
        "yards_scrimmage" : "player_stats_utils.clean_stat(yr_row.find('td', {'data-stat' : 'yds_from_scrimmage'}).string)"
    }
    return stat_calc_dict

def get_calculated_stats_dict(dictionary_name):
    
    calculated_stat_dict = {
        "catch_perc" : "player_stats_utils.clean_divided_stat(" + dictionary_name + "['agg_{time_range}_rec'.format(**locals())," + dictionary_name + "['agg_{time_range}_targets'.format(**locals())])",
        "pass_adj_yds_per_att" : "player_stats_utils.clean_divided_stat(" + dictionary_name + "['agg_{time_range}_pass_yds'.format(**locals())] + ( (20 * float(" + dictionary_name + "['agg_{time_range}_pass_yds'.format(**locals())])) - (45 * " + dictionary_name + "['agg_{time_range}_pass_yds'.format(**locals())])))," + + "['agg_{time_range}_pass_yds'.format(**locals())])",
        "pass_comp_pct" : "clean_divided_stat(" + dictionary_name + "['agg_{time_range}_pass_comp'.format(**locals())], " + dictionary_name + "['agg_{time_range}_pass_att'.format(**locals())])",
        "pass_yds_per_att" : "clean_divided_stat(" + dictionary_name + "['agg_{time_range}_pass_yds'.format(**locals())] , " + dictionary_name + "['agg_{time_range}_pass_att'.format(**locals())])",
        "pass_td_perc" : "clean_divided_stat(" + dictionary_name + "['agg_{time_range}_pass_tds'.format(**locals())], " + dictionary_name + "['agg_{time_range}_pass_att'.format(**locals())])",
        "pass_int_perc" : "clean_divided_stat(" + dictionary_name + "['agg_{time_range}_pass_int'.format(**locals())], " + dictionary_name + "['agg_{time_range}_pass_att'.format(**locals())])",
        "rush_yds_per_att" : "clean_divided_stat(" + dictionary_name + "['agg_{time_range}_rush_yds'.format(**locals())], " + dictionary_name + "['agg_{time_range}_rush_att'.format(**locals())])",
        "rush_yds_per_game" : "clean_divided_stat(" + dictionary_name + "['agg_{time_range}_rush_yds'.format(**locals())], " + dictionary_name + "['agg_{time_range}_games'.format(**locals())])",
        "rush_att_per_game" : "clean_divided_stat(" + dictionary_name + "['agg_{time_range}_rush_att'.format(**locals())],  " + dictionary_name + "['agg_{time_range}_games'.format(**locals())])",
        "rec_yds_per_catch" : "clean_divided_stat(" + dictionary_name + "['agg_{time_range}_rec_yds'.format(**locals())], " + dictionary_name + "['agg_{time_range}_rec'.format(**locals())])",
        "recs_per_game" : "clean_divided_stat(" + dictionary_name + "['agg_{time_range}_rec'.format(**locals())], " + dictionary_name + "['agg_{time_range}_games'.format(**locals())])",
        "rec_yds_per_game" : "clean_divided_stat(" + dictionary_name + "['agg_{time_range}_rec_yds'.format(**locals())], " + dictionary_name + "['agg_{time_range}_games'.format(**locals())])",
        "sacked_perc" : "clean_divided_stat(" + dictionary_name + "['agg_{time_range}_sacked'.format(**locals())], (" + dictionary_name + "['agg_{time_range}_sacked'.format(**locals())] + " + dictionary_name + "['agg_{time_range}_pass_att'.format(**locals())]))" 
    }
    
    return calculated_stat_dict
    
        #if final_tbl_id == 'passing':
        #    pass_stats = get_passing_stats(player_stats, ranges_dict)
        #    player_dict['stats'].update(pass_stats)
#        if final_tbl_id in ['rushing_and_receiving', 'receiving_and_rushing'] :
#            if standardized_pos in ["G", "T", "C"]:
#                rush_rec_stats =  get_ol_def_stats(player_stats, ranges_dict, side)
#            else:
#                rush_rec_stats = get_rush_rec_stats(player_stats, ranges_dict, standardized_pos) 
#                
#            player_dict['stats'].update(rush_rec_stats)
#        if final_tbl_id in ['defense', 'games_played', 'returns']:
#            side = position_dict[standardized_pos]["primary_side"]
#            ol_def_stats = get_ol_def_stats(player_stats, ranges_dict, side)
#            
#            if standardized_pos in ["RB", "WR", "TE"]:
#                ol_def_stats = append_skill_pos_stats(ol_def_stats, ranges_dict, standardized_pos)
#
#            player_dict['stats'].update(ol_def_stats)
#                
#    else: ## standardized_pos == "QB"
#        for tbl_id in player_stats_table_id_list:
#            try:            
#                player_stats = player_soup.find(id=tbl_id).tbody
#                player_stat_rows = player_stats.findAll('tr')
#            except AttributeError:
#                player_stats = None
#                player_stat_rows = []
#    
#
#            team_abbr = team_abbr_dict.keys()[team_abbr_dict.values().index(team)]   
#
#            if tbl_id == 'passing':
#                yrs_w_team, yrs_career, age = get_yrs_experience(player_stat_rows, year, team_abbr)
#                player_dict['stats'].update({
#                    'yrs_w_team' : yrs_w_team,
#                    'yrs_career' : yrs_career,
#                    'age'        : age
#                })
#                pass_stats = get_passing_stats(player_stats, ranges_dict)
#                player_dict['stats'].update(pass_stats)
#            if tbl_id in ['rushing_and_receiving', 'receiving_and_rushing', 'defense'] :
#                rush_rec_stats = get_rush_rec_stats(player_stats, ranges_dict, standardized_pos)    
#                player_dict['stats'].update(rush_rec_stats)

    
def get_final_tbl_id(standardized_pos, player_soup):
    
    tbl_id_list = ["games_played", "defense", "receiving_and_rushing", "rushing_and_receiving", "returns"]

    tbl_count_dict = {}        
    for table_id in tbl_id_list:
        try:            
            temp_tag = player_soup.find(id=table_id).tbody
            temp_tag_rows = temp_tag.findAll('tr')
            tbl_count_dict[table_id] = len(temp_tag_rows)
        except AttributeError:
            tbl_count_dict[table_id] = 0
            
    max_rows = 0
    for k, v in tbl_count_dict.iteritems():
        if v > max_rows:
            max_rows = v
            
    if standardized_pos in ["RB"]:
        if tbl_count_dict['rushing_and_receiving'] == max_rows:
            final_tbl_id = 'rushing_and_receiving'
        else:
            final_tbl_id = max(tbl_count_dict.iteritems(), key=operator.itemgetter(1))[0]
    elif standardized_pos in ["WR", "TE"]:
        if tbl_count_dict['receiving_and_rushing'] == max_rows:
            final_tbl_id = 'receiving_and_rushing'
        else:
            final_tbl_id = max(tbl_count_dict.iteritems(), key=operator.itemgetter(1))[0]
        #final_tbl_id = "receiving_and_rushing"
                
    else: 
        final_tbl_id = max(tbl_count_dict.iteritems(), key=operator.itemgetter(1))[0]

    return final_tbl_id