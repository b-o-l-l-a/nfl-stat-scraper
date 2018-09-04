game_pass_stats = [
    "pass_cmp", "pass_att", "pass_yds", "pass_td" \
    "pass_td", "pass_int", "pass_sacked", "pass_sacked_yds" \
    "pass_long", "pass_rating", "fumbles", "fumbles_lost"
]

game_rush_stats = [
    "rush_att", "rush_yds", "rush_td", "rush_long", "fumbles", "fumbles_lost"
]

game_rec_stats = [
    "targets", "rec", "rec_yds", "rec_td", "rec_long", "fumbles", "fumbles_lost"
]

game_def_tackle_stats = [
    "sacks", "tackles_solo", "tackles_assists", "fumbles_forced", "fumbles_rec"
]

game_def_int_stats = [
    "def_int", "fumbles_forced", "fumbles_recs"
]

game_kicking_stats = [
    "xpm", "xpa", "fgm", "fga"
]

game_punting_stats = [
    "punt", "punt_yds_per_punt"
]

class OffLineman():
    def __init__(self, PlayerGame):
        
        return
    def get_positional_stats(self, PlayerGame):
        
        return {}

class Quarterback():
    def __init__(self, PlayerGame):
        
        self.game_tbl_passing_stats = game_pass_stats
        self.game_tbl_rushing_stats = game_rush_stats
    
    def get_positional_stats(self, PlayerGame):
        
        
        positional_stats_list = self.game_tbl_passing_stats + self.game_tbl_rushing_stats
        
        qb_stats = PlayerGame.get_player_indiv_game_stats(positional_stats_list)
        
        return qb_stats
    
class RunningBack():
    def __init__(self, PlayerGame):
        
        self.game_tbl_rushing_stats = game_rush_stats
        self.game_tbl_rec_stats = game_rec_stats
        
    
    def get_positional_stats(self, PlayerGame):
        
        positional_stats_list = self.game_tbl_rushing_stats + self.game_tbl_rec_stats
        rb_stats = PlayerGame.get_player_indiv_game_stats(positional_stats_list)

        return rb_stats

class WideReceiver():
    def __init__(self, PlayerGame):
        
        self.game_tbl_rushing_stats = game_rush_stats
        self.game_tbl_rec_stats = game_rec_stats
        
    
    def get_positional_stats(self, PlayerGame):

        positional_stats_list = self.game_tbl_rushing_stats + self.game_tbl_rec_stats
        wr_stats = PlayerGame.get_player_indiv_game_stats(positional_stats_list)

        return wr_stats
    
class TightEnd():
    def __init__(self, PlayerGame):
        
        self.game_tbl_rec_stats = game_rec_stats
        
    def get_positional_stats(self, PlayerGame):

        positional_stats_list = self.game_tbl_rec_stats  
        te_stats = PlayerGame.get_player_indiv_game_stats(positional_stats_list)

        return te_stats

class DefLineman():

    def __init__(self, PlayerGame):
        
        self.game_tbl_def_stats = game_def_tackle_stats
        
    def get_positional_stats(self, PlayerGame):

        positional_stats_list = self.game_tbl_def_stats  
        dl_stats = PlayerGame.get_player_indiv_game_stats(positional_stats_list)

        return dl_stats
    
class Linebacker():

    def __init__(self, PlayerGame):
        
        self.game_tbl_def_stats = game_def_tackle_stats + game_def_int_stats
        
    def get_positional_stats(self, PlayerGame):

        positional_stats_list = self.game_tbl_def_stats  
        lb_stats = PlayerGame.get_player_indiv_game_stats(positional_stats_list)

        return lb_stats

class DefBack():
    
    def __init__(self, PlayerGame):
        
        self.game_tbl_def_stats = game_def_tackle_stats + game_def_int_stats
        
    def get_positional_stats(self, PlayerGame):

        positional_stats_list = self.game_tbl_def_stats  
        db_stats = PlayerGame.get_player_indiv_game_stats(positional_stats_list)

        return db_stats
    
class Kicker():
    
    def __init__(self, PlayerGame):
        
        self.game_tbl_k_stats = game_kicking_stats
        
    def get_positional_stats(self, PlayerGame):

        positional_stats_list = self.game_tbl_k_stats  
        k_stats = PlayerGame.get_player_indiv_game_stats(positional_stats_list)

        return k_stats
    
class Punter():
    
    def __init__(self, PlayerGame):
        
        self.game_tbl_p_stats = game_punting_stats
        
    def get_positional_stats(self, PlayerGame):

        positional_stats_list = self.game_tbl_p_stats  
        p_stats = PlayerGame.get_player_indiv_game_stats(positional_stats_list)

        return p_stats