# -*- coding: utf-8 -*-
"""
Created on Fri Sep 08 20:36:29 2017

@author: greg.bolla
"""
import requests
from bs4 import BeautifulSoup
import re
from player_stat_utils import clean_stat

def get_weekly_def_stats(gamelog_base_url, gamelog_stat_rows, current_game, year, week):
    final_tbl_id = "stats"
    
    row = {}
    
    for prev_wks in ["2", "4", "6"]:
        
        games = \
        def_int = \
        def_int_yds = \
        def_int_tds = \
        def_pd = \
        forced_fum = \
        sacks = \
        tackles = \
        assists = 0
        
        #print("current game: {} / prev_wks : {}".format(current_game, prev_wks))
        start_game = int(current_game) - int(prev_wks)
        prev_yr_flg = False
        if start_game < 0:
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
            
            try :
                prev_yr_gamelog_stats = prev_yr_gamelog_soup.find(id="stats").tbody
                prev_yr_gamelog_stat_rows = prev_yr_gamelog_stats.findAll('tr')
            
                for game in prev_yr_gamelog_stat_rows:
                    if int(game.find('td', {'data-stat' : 'game_num'}).string) >= start_game:
                        games += 1
                        try: def_int += clean_stat(game.find('td', {'data-stat' : 'def_int'}).string) 
                        except AttributeError: pass
                        try: def_int_yds += clean_stat(game.find('td', {'data-stat' : 'def_int_yds'}).string) 
                        except AttributeError: pass
                        try: def_int_tds += clean_stat(game.find('td', {'data-stat' : 'def_int_tds'}).string) 
                        except AttributeError: pass
                        try: sacks += clean_stat(game.find('td', {'data-stat' : 'sacks'}).string) 
                        except AttributeError: pass
                        try: 
                            tackles += clean_stat(game.find('td', {'data-stat' : 'tackles_solo'}).string) 
                        except AttributeError: pass
                        try: 
                            assists += clean_stat(game.find('td', {'data-stat' : 'tackles_assists'}).string) 
                        except AttributeError: pass 
                           
            except AttributeError: 
                print("no stats in prev year")                
                pass
        #else:
        for game in gamelog_stat_rows:
            calc_row_flg = False
            if prev_yr_flg == True:
                if int(game.find('td', {'data-stat' : 'game_num'}).string) < int(current_game): 
                    calc_row_flg = True
                else:
                    calc_row_flg = False
            else:
                row_game_num = int(game.find('td', {'data-stat' : 'game_num'}).string)
                if row_game_num < int(current_game) and row_game_num >= start_game:
                    calc_row_flg = True
                else: 
                    calc_row_flg = False
            
            if calc_row_flg == True:
                games += 1
                try: def_int += clean_stat(game.find('td', {'data-stat' : 'def_int'}).string) 
                except AttributeError: pass
                try: def_int_yds += clean_stat(game.find('td', {'data-stat' : 'def_int_yds'}).string) 
                except AttributeError: pass
                try: def_int_tds += clean_stat(game.find('td', {'data-stat' : 'def_int_tds'}).string) 
                except AttributeError: pass
                try: sacks += clean_stat(game.find('td', {'data-stat' : 'sacks'}).string) 
                except AttributeError: pass
                try: tackles += clean_stat(game.find('td', {'data-stat' : 'tackles_solo'}).string) 
                except AttributeError: pass
                try: assists += clean_stat(game.find('td', {'data-stat' : 'tackles_assists'}).string) 
                except AttributeError: pass 
                
        row["prev{}wks_games".format(prev_wks)] = games                
        row["prev{}wks_def_int".format(prev_wks)] = def_int
        row["prev{}wks_def_int_yds".format(prev_wks)] = def_int_yds
        row["prev{}wks_def_int_td".format(prev_wks)] = def_int_tds
        row["prev{}wks_sacks".format(prev_wks)] = sacks
        row["prev{}wks_tackles".format(prev_wks)] = tackles
        row["prev{}wks_assists".format(prev_wks)] = assists
        
    return row        

def get_weekly_ol_stats(gamelog_base_url, gamelog_stat_rows, current_game, year, week):
    final_tbl_id = "stats"
    
    row = {}
    
    for prev_wks in ["2", "4", "6"]:
        
        games = 0
        
        #print("current game: {} / prev_wks : {}".format(current_game, prev_wks))
        start_game = int(current_game) - int(prev_wks)
        prev_yr_flg = False
        if start_game < 0:
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
            try :
                prev_yr_gamelog_stats = prev_yr_gamelog_soup.find(id="stats").tbody
                prev_yr_gamelog_stat_rows = prev_yr_gamelog_stats.findAll('tr')
            
                for game in prev_yr_gamelog_stat_rows:
                    if int(game.find('td', {'data-stat' : 'game_num'}).string) >= start_game:
                        games += 1
                            
            except AttributeError: 
                print("no stats in prev year")                
                pass
        #else:
        for game in gamelog_stat_rows:
            calc_row_flg = False
            if prev_yr_flg == True:
                if int(game.find('td', {'data-stat' : 'game_num'}).string) < int(current_game): 
                    calc_row_flg = True
                else:
                    calc_row_flg = False
            else:
                row_game_num = int(game.find('td', {'data-stat' : 'game_num'}).string)
                if row_game_num < int(current_game) and row_game_num >= start_game:
                    calc_row_flg = True
                else: 
                    calc_row_flg = False
            
            if calc_row_flg == True:
                games += 1
                
        row["prev{}wks_games".format(prev_wks)] = games                

    return row        
