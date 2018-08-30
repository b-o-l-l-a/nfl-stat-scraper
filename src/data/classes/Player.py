from classes.Positions import OffLineman, Quarterback, RunningBack, WideReceiver, TightEnd, DefLineman, Linebacker, DefBack, Kicker, Punter

class PlayerGame():
    def __init__(self, Team, player_name, player_link, position):
        
        self.min_snap_perc = .10
        self.name = player_name
        self.player_link = player_link   
        self.game_html_page = Team.game_html_page
        self.season = Team.season
        self.week = Team.week
        self.team = Team.team
        self.team_abbrev = Team.team_abbrev
        self.base_url = Team.base_url
        self.full_player_url = self.base_url + player_link
        self.standardized_position_dict = {
            "OL" : {"eligible_positions" : ["G", "T", "C", "LS"], 
                   "class": OffLineman,
                   "side" : "offense"},
            "QB" : {"eligible_positions" : ["QB"], 
                   "class": Quarterback,
                   "side" : "offense"},
            "WR" : {"eligible_positions" : ["WR"],
                   "class": WideReceiver,
                   "side" : "offense"},
            "TE" : {"eligible_positions" : ["TE"],
                   "class": TightEnd,
                   "side" : "offense"},
            "RB" : {"eligible_positions" : ["RB", "FB"],
                   "class": RunningBack,
                   "side" : "offense"},
            "DB" : {"eligible_positions" : ["SS", "FS", "CB", "DB"],
                   "class": DefBack,
                   "side" : "defense"},
            "LB" : {"eligible_positions" : ["LB", "OLB", "MLB"],
                   "class": Linebacker,
                   "side" : "defense"},
            "DL" : {"eligible_positions" : ["DT", "DL", "NT", "DE"],
                   "class": DefLineman,
                   "side" : "defense"},
            "K" : {"eligible_positions" : ["K"],
                   "class": Kicker,
                   "side" : "special_teams"},
            "P" : {"eligible_positions" : ["P"],
                   "class": Punter,
                   "side" : "special_teams"}
        }
        
        self.standardized_pos = [k for k, v in self.standardized_position_dict.items() \
                                 if position in v["eligible_positions"]][0]
        self.player_class = self.standardized_position_dict[self.standardized_pos]["class"]
        self.side = self.standardized_position_dict[self.standardized_pos]['side']

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