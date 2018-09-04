import pandas as pd
import os 

from classes.Player import Player
from utils import dict_to_csv

def get_player_data():
    
    player_filename = 'game_summary_by_player.csv'
    data_dir = os.getcwd() + '/data/external'
    player_path = os.path.join(data_dir, player_filename)
    output_path = os.path.join(data_dir, 'player_metadata.csv')
    
    player_game_df = pd.read_csv(player_path)
    players_df = player_game_df[["player_link", "player_name"]].drop_duplicates()
    
    if os.path.isfile(player_path):
        addtl_rows_flg = True
        player_metadata_df = pd.read_csv(output_path)
        player_metadata_df = player_metadata_df.drop_duplicates()
    else:
        addtl_rows_flg = False
        player_metadata_df = pd.DataFrame()
    
    if addtl_rows_flg == True:
        existing_players = list(player_metadata_df["player_link"].unique())
        print(player_metadata_df.tail())
        print(players_df.head())
        players_df = players_df[~players_df["player_link"].isin(existing_players)]
        print("number of players already scraped: {} / length of remaining df: {}".format(len(existing_players), len(players_df)))
    output_rows = []
    for idx, row in players_df.iterrows():
        name = row['player_name']
        link = row['player_link']
        print("{}: {} - {}".format(idx, name, link))
        player = Player(name, link)
        
        #print("{}: {} - {}".format(idx, player.name, player.full_player_url))
        player_dict = player.get_player_data() 
        dict_to_csv(player_dict, data_dir, 'player_metadata')
        output_rows.append(player_dict)
        

    
    #output_df = pd.DataFrame(output_rows)
    #output_path = os.path.join(data_dir, 'player_metadata.csv' )
    
    #output_df = output_df[["player_link", "player_name", "position", "draft_pick" ,"height", "weight", "height", "birthdate", "forty_yd", "combine_bench", "combine_broad_jump", "combine_cone", "combine_shuttle", "combine_vert", "combine_year"]]
    
    #output_df.to_csv(output_path, index = False)
    return

if __name__ == "__main__":
    
    get_player_data()
    