from bs4 import BeautifulSoup, NavigableString
import datetime
import re
import os

from classes.Positions import OffLineman, Quarterback, RunningBack, WideReceiver, TightEnd, DefLineman, Linebacker, DefBack, Kicker, Punter
from utils import get_html, get_config

class Player():
    def __init__(self, player_name, player_link,  Team = None, position = None):
        
        self.min_snap_perc = .10
        self.name = player_name
        self.player_link = player_link  
        
        config = get_config(os.getcwd())
        self.base_url = config['base_url']
        self.full_player_url = self.base_url + player_link
        self.standardized_position_dict = {
            "OL" : {"eligible_positions" : ["G", "T", "C", "LS", "OT", "OG", "OL","G/C", "G-C", "T-G", "G-T", "C-G", "G,C", "C,G", "G,T", "T,G"], 
                   "class": OffLineman,
                   "side" : "offense"},
            "QB" : {"eligible_positions" : ["QB"], 
                   "class": Quarterback,
                   "side" : "offense"},
            "WR" : {"eligible_positions" : ["WR", "PR-WR", "WR/RB"],
                   "class": WideReceiver,
                   "side" : "offense"},
            "TE" : {"eligible_positions" : ["TE", "LS,TE", "TE-C"],
                   "class": TightEnd,
                   "side" : "offense"},
            "RB" : {"eligible_positions" : ["RB", "FB", "FB-LB", "HB"],
                   "class": RunningBack,
                   "side" : "offense"},
            "DB" : {"eligible_positions" : ["SS", "FS", "CB", "DB", "S"],
                   "class": DefBack,
                   "side" : "defense"},
            "LB" : {"eligible_positions" : ["LB", "OLB", "ILB", "MLB", "LB-DE"],
                   "class": Linebacker,
                   "side" : "defense"},
            "DL" : {"eligible_positions" : ["DT", "DL", "NT", "DE", "NT-DT", "DT-NT", "DE-LB", "DT/LB", "DE-C", "DE-DT", "DT-DE"],
                   "class": DefLineman,
                   "side" : "defense"},
            "K" : {"eligible_positions" : ["K"],
                   "class": Kicker,
                   "side" : "special_teams"},
            "P" : {"eligible_positions" : ["P"],
                   "class": Punter,
                   "side" : "special_teams"}
        }
        
        
        if Team is not None:
            self.game_html_page = Team.game_html_page
            self.season = Team.season
            self.week = Team.week
            self.team = Team.team
            self.team_abbrev = Team.team_abbrev
            self.base_url = Team.base_url
        
        if position is None:
            self.player_page = get_html(self.full_player_url)
            self.meta_div = self.player_page.find("div", {"itemtype" : "https://schema.org/Person"})
            position = self.get_position_from_player_page(self.meta_div)
        
        self.standardized_pos = [k for k, v in self.standardized_position_dict.items() \
                                 if position in v["eligible_positions"]][0]
        self.player_class = self.standardized_position_dict[self.standardized_pos]["class"]
        self.side = self.standardized_position_dict[self.standardized_pos]['side']

    def get_position_from_player_page(self, metadata_div):
        pattern = re.compile(r'Position')
        if metadata_div.find('strong', text=pattern) is None:
            if self.name == "Virgil Green":
                position = "TE"
            elif self.name == "Vincent Brown":
                position = "WR"
            elif self.name == "Michael Davis":
                position = "DB"
        else:
          
            tag = metadata_div.find('strong', text=pattern).parent
            for child in tag:
                if isinstance(child, NavigableString) and ":" in child:
                    position = child.split(":")[-1].strip()
            
        return position

    def get_player_summary(self):
    
        player_dict = {}
        
        player_dict["player_name"] = self.name       
        player_dict["player_link"] = self.player_link
        player_dict["team"] = self.team
        player_dict["season"] = self.season 
        player_dict["week"] = self.week
        player_dict["position"] = self.standardized_pos

        return player_dict
    
    def get_snaps(self, tr):
        
        if self.side == "offense":
            perc_snaps_id = "off_pct"
        elif self.side == "defense":
            perc_snaps_id = "def_pct"
        elif self.side == "special_teams":
            perc_snaps_id = "st_pct"
        perc_snaps_str = tr.find("td", {"data-stat" : perc_snaps_id}).string
        perc_snaps = float(int(perc_snaps_str.replace("%","")) / 100)
        
        num_snaps = tr.find("td", {"data-stat" : self.side}).string
        
        return num_snaps, perc_snaps
    
    def get_player_indiv_game_stats(self, positional_stats_list):
        
#         game_html = self.game_html
#         player_link = self.player_link
#         side = self.side
       
#         if side in ["defense", "offense"]:
#             game_stats_id = "player_{}".format(side)
#         elif side in ["special_teams"]:
#             game_stats_id = "kicking"

#         game_stats_tbody = game_html.find("table", {"id" : game_stats_id}).tbody
        
        player_game_stats = self.get_player_game_stats()
        indiv_player_stats_dict = {}
        #if game_stats_tbody.find("a", {"href" : player_link}) is not None:
        #game_stats_row = game_stats_tbody.find("a", {"href" : player_link}).parent.parent
        player_stats = player_game_stats.findAll('td')    
        player_stats = list(filter(lambda x: x["data-stat"] in positional_stats_list, player_stats))

        for td in player_stats:
            indiv_player_stats_dict[td["data-stat"]] = td.string 
        #else:
        #    for stat in game_stats_list:
        #        indiv_player_stats_dict[stat] = 0
                
        return indiv_player_stats_dict

    def get_player_game_stats(self):
        
        game_html = self.game_html_page
        player_link = self.player_link
        side = self.side        
        
        if side in ["defense", "offense"]:
            game_stats_id = "player_{}".format(side)
        elif side in ["special_teams"]:
            game_stats_id = "kicking"

        game_stats_tbody = game_html.find("table", {"id" : game_stats_id}).tbody
        
        if game_stats_tbody.find("a", {"href" : player_link}) is None:
            player_game_stats = None
        else:
            player_game_stats = game_stats_tbody.find("a", {"href" : player_link}).parent.parent
            
        return player_game_stats
    
    def get_pos_stats_flg(self, player_snaps_tr):
        
        player_game_stats = self.get_player_game_stats()
        player_game_stats_flg = True if player_game_stats is not None else False
        
        num_snaps, perc_snaps = self.get_snaps(player_snaps_tr)
        perc_snaps_flg = True if perc_snaps >= self.min_snap_perc else False
        
        pos_stats_flg = all([player_game_stats_flg, perc_snaps_flg])
        return pos_stats_flg
    
    def get_player_data(self):
        
        player_data = {}
        player_data['player_link'] = self.player_link
        player_data['player_name'] = self.name
        player_data['position'] = self.standardized_pos
        
        player_metadata = self.get_player_metadata()
        player_combine_data = self.get_combine_data()
        
        player_data.update(player_metadata)
        player_data.update(player_combine_data)
        
        return player_data
    
    def get_combine_data(self):
        
        combine_tbl = self.player_page.find("table", {"id": "combine"})
        combine_dict = {}
        
        if combine_tbl is not None:
            combine_row = combine_tbl.tbody.tr
            combine_yr = combine_row.find("th", {"data-stat" : "year_id"}).a.string
            combine_height = combine_row.find("td", {"data-stat" : "height"}).string
            combine_weight = combine_row.find("td", {"data-stat" : "weight"}).string
            combine_forty = combine_row.find("td", {"data-stat" : "forty_yd"}).string
            combine_bench = combine_row.find("td", {"data-stat" : "bench_reps"}).string
            combine_broad_jump = combine_row.find("td", {"data-stat" : "broad_jump"}).string
            combine_shuttle = combine_row.find("td", {"data-stat" : "shuttle"}).string
            combine_cone = combine_row.find("td", {"data-stat" : "cone"}).string
            combine_vert = combine_row.find("td", {"data-stat" : "vertical"}).string
            
            combine_dict['combine_year'] = combine_yr
            combine_dict['height'] = combine_height
            combine_dict['weight'] = combine_weight
            combine_dict['forty_yd'] = combine_forty
            combine_dict['combine_bench'] = combine_bench
            combine_dict['combine_broad_jump'] = combine_broad_jump
            combine_dict['combine_shuttle'] = combine_shuttle
            combine_dict['combine_cone'] = combine_cone
            combine_dict['combine_vert'] = combine_vert
            
        return combine_dict
    def get_player_metadata(self):
        
        player_metadata_dict = {}
        player_page = self.player_page
        birthdate_string = player_page.find("span", {"itemprop":"birthDate"})['data-birth']
        birthdate = datetime.datetime.strptime(birthdate_string, '%Y-%m-%d')
        player_metadata_dict['birthdate'] = birthdate
        
        draft_pick = self.get_draft_pick()
        player_metadata_dict['draft_pick'] = draft_pick        
        
        return player_metadata_dict
    
    def get_draft_pick(self):
        meta_div = self.meta_div
        draft_pattern = re.compile(r'Draft')        
        
        if meta_div.find('strong', text=draft_pattern) is None:
            draft_pick = None
        else:
            draft_tag = meta_div.find('strong', text=draft_pattern).parent
        
            for child in draft_tag.children:

                # check to see if child is a string, and check to see if there are parentheses within that string
                if isinstance(child, NavigableString) and re.search(r'\((.*?)\)',child) is not None:

                    re_draft_pick = re.search(r'\((.*?)\)',child)            
                    draft_pick_string = re_draft_pick.group(1)

                    # in the string that specifies draft pick, grab the number before ordinal string
                    draft_pick = re.search(r'.+?(?=[st|nd|rd|th])', draft_pick_string).group(0)
                    draft_pick = int(draft_pick)
                    
        return draft_pick
        
        