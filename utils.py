# -*- coding: utf-8 -*-
"""
Created on Sun Jul 09 16:04:46 2017

@author: greg.bolla
"""

import pandas as pd

def get_full_team_names():
    team_dict = {
        "ATL" : "Atlanta Falcons",
        "ARI" : "Arizona Cardinals",
        "BAL" : "Baltimore Ravens",
        "BUF" : "Buffalo Bills",
        "CAR" : "Carolina Panthers",
        "CHI" : "Chicago Bears",
        "CIN" : "Cincinnati Bengals",
        "CLE" : "Cleveland Browns",
        "DAL" : "Dallas Cowboys",
        "DEN" : "Denver Broncos",
        "DET" : "Detroit Lions",
        "GNB" : "Green Bay Packers",
        "HOU" : "Houston Texans",
        "IND" : "Indianapolis Colts",
        "JAX" : "Jacksonville Jaguars",
        "KAN" : "Kansas City Chiefs",
        "LAR" : "Los Angeles Rams", 
        "MIA" : "Miami Dolphins",
        "MIN" : "Minnesota Vikings",
        "NWE" : "New England Patriots",
        "NYG" : "New York Giants",
        "NYJ" : "New York Jets",
        "NOR" : "New Orleans Saints",
        "OAK" : "Oakland Raiders",
        "PHI" : "Philadelphia Eagles",
        "PIT" : "Pittsburgh Steelers",
        "SDG" : "San Diego Chargers",
        "SDG" : "Los Angeles Chargers",
        "SEA" : "Seattle Seahawks",
        "SFO" : "San Francisco 49ers",
        "STL" : "St. Louis Rams",
        "TAM" : "Tampa Bay Buccaneers",
        "TEN" : "Tennessee Titans",
        "WAS" : "Washington Redskins"
    }
    
    return team_dict

def combine_csvs(wd = "C:\\Users\\greg.bolla\\Desktop\\Personal\\Football Spreads"):
    start_yr = 2008
    end_yr = 2017
    
    full_predictor_df = pd.DataFrame()
    
    redo_csv = pd.read_csv("{wd}\\new_player_stats\\additional_positional_predictors.csv".format(**locals()))
    for year in range(start_yr, end_yr):
    #for year in [2008, 2009, 20]:
        yearly_predictor_df = pd.DataFrame()
        year_string = str(year)
        #path = "{}\\{}\\".format(wd, year_string)
        
        print("combining for year: {year_string}".format(**locals()))
        for week in range(1, 18):
            week_string = str(week)
            weekly_predictor_df = pd.read_csv("{wd}\\new_player_stats\\{year_string}\\positional_predictors_{year_string}_week{week_string}.csv".format(**locals()))
            yearly_predictor_df = yearly_predictor_df.append(weekly_predictor_df)
        
        yearly_predictor_df.to_csv("{wd}\\new_player_stats\\{year_string}\\positional_predictors_{year_string}_full.csv".format(**locals()))
        full_predictor_df = full_predictor_df.append(yearly_predictor_df)
    
    full_predictor_df = full_predictor_df.append(redo_csv)
    full_predictor_df.to_csv("{wd}\\new_player_stats\\positional_predictors_full.csv".format(**locals()), index = False)