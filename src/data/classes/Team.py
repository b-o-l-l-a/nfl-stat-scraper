import pandas as pd
import os

class Team():
    def __init__(self, Game, team_name, opponent, home_flg):
        
        self.game_html_page = Game.game_html_page
        self.season = Game.season
        self.week = Game.week
        self.base_url = Game.base_url
        self.team_table_id = "home" if home_flg == True else "vis"
        self.opp_table_id =  "vis" if home_flg == True else "home"
        self.home_flg = home_flg
        self.team = team_name
        self.opponent = opponent
        self.team_abbrev = self.get_team_abbrev(opponent_flg = False)
        self.opp_abbrev = self.get_team_abbrev(opponent_flg = True)
        self.data_dir = os.path.join(os.getcwd(), "data", "external")
        self.num_wks_to_find = 3
        
    def get_team_abbrev(self, opponent_flg):
        
        team = self.team if opponent_flg == False else self.opponent
        
        team_abbrev_dict = {
            "Atlanta Falcons" : "ATL",
            "Arizona Cardinals" : "ARI",
            "Baltimore Ravens" : "BAL",
            "Buffalo Bills" : "BUF",
            "Carolina Panthers" : "CAR",
            "Chicago Bears" : "CHI",
            "Cincinnati Bengals" : "CIN",
            "Cleveland Browns" : "CLE",
            "Dallas Cowboys" : "DAL",
            "Denver Broncos" : "DEN",
            "Detroit Lions" : "DET",
            "Green Bay Packers" : "GNB",
            "Houston Texans" : "HOU",
            "Indianapolis Colts" : "IND",
            "Jacksonville Jaguars" : "JAX",
            "Kansas City Chiefs" : "KAN",
            "Los Angeles Chargers" : "LAC",
            "Los Angeles Rams": "LAR",
            "Miami Dolphins" : "MIA",
            "Minnesota Vikings" : "MIN",
            "New England Patriots" : "NWE",
            "New Orleans Saints" : "NOR",
            "New York Giants" : "NYG",
            "New York Jets" : "NYJ",
            "Oakland Raiders" : "OAK",
            "Philadelphia Eagles" : "PHI",
            "Pittsburgh Steelers" : "PIT",
            "San Diego Chargers" : "SDG",
            "San Francisco 49ers" : "SFO",
            "Seattle Seahawks" : "SEA",
            "St. Louis Rams" : "STL",
            "Tampa Bay Buccaneers" : "TAM",
            "Tennessee Titans" : "TEN",
            "Washington Redskins" : "WAS"
        }
        
        abbrev = team_abbrev_dict[team]
        return abbrev
    
    def get_team_game_summary(self, Game):
        
        game_summary_dict = Game.game_summary_dict
        team_favored = True if Game.favorite == self.team else False
        team_win = True if game_summary_dict["winner"] == self.team else False
        #team_home = True if game_summary_dict["home_team"] == self.team else False
        
        team_game_summary_dict = {}
        team_game_summary_dict["url"] = Game.game_url_append
        team_game_summary_dict["season"] = Game.season
        team_game_summary_dict["week"] = Game.week
        team_game_summary_dict["team"] = self.team
        team_game_summary_dict["opponent"] = self.opponent
        team_game_summary_dict["home_flg"] = self.home_flg
        team_game_summary_dict["favorite_flg"] = team_favored
        team_game_summary_dict["winner_flg"] = team_win
        team_game_summary_dict["line"] = (-1 * abs(float(Game.line))) if team_favored else abs(float(Game.line))
        team_game_summary_dict["over_under"] = Game.over_under
        team_game_summary_dict["off_pts"] = game_summary_dict["pts_win"] if team_win else game_summary_dict["pts_lose"]
        team_game_summary_dict["def_pts_allowed"] = game_summary_dict["pts_lose"] if team_win else game_summary_dict["pts_win"]
        return team_game_summary_dict 
        
        
    def get_indiv_game_stats(self):
        game_stats_id = "team_stats"
        game_html = self.game_html_page
        stats_table = game_html.find(id=game_stats_id).tbody
        stats_table_rows = stats_table.findAll('tr')

        stats_table_dict = {}       
        
        for tr in stats_table_rows:
            stats_table_dict = self.clean_stats_table_row(tr, stats_table_dict)
    
        return stats_table_dict
    
    def get_drive_summary_dict(self):
        game_html = self.game_html_page
        
        team_id = "{}_drives".format(self.team_table_id)
        opp_id = "{}_drives".format(self.opp_table_id)
        
        team_drive_tbl = game_html.find("table", {"id" : team_id}).tbody
        opp_drive_tbl = game_html.find("table", {"id" : opp_id}).tbody
        
        drive_summary_dict = {}
        drive_summary_dict = self.build_team_drive_summary_dict(drive_summary_dict, team_drive_tbl, team_flg = True)
        drive_summary_dict = self.build_team_drive_summary_dict(drive_summary_dict, opp_drive_tbl, team_flg = False)

        return drive_summary_dict

    def build_team_drive_summary_dict(self, drive_summary_dict, drive_tbl, team_flg):
        
        drive_rows = drive_tbl.findAll("tr")
        num_drives = len(drive_rows)
        num_yds = 0
        num_tds = 0
        num_fgs = 0
        num_plays = 0
        num_punts = 0
        for tr in drive_rows:
            plays = int(tr.find("td", {"data-stat": "play_count_tip"}).span.string)
            num_plays += plays
            
            yds = int(tr.find("td", {"data-stat": "net_yds"}).string)
            num_yds += yds
            
            end_evt = tr.find("td", {"data-stat": "end_event"}).string
            
            if end_evt == "Punt":
                num_punts += 1
            elif end_evt == "Field Goal":
                num_fgs += 1
            elif end_evt == "Touchdown":
                num_tds += 1
        
        col_prepend = "team" if team_flg == True else "opp"
        
        drive_summary_dict["{}_drives".format(col_prepend)] = num_drives
        drive_summary_dict["{}_plays".format(col_prepend)] = num_plays
        drive_summary_dict["{}_yds".format(col_prepend)] = num_yds
        drive_summary_dict["{}_tds".format(col_prepend)] = num_tds
        drive_summary_dict["{}_fgs".format(col_prepend)] = num_fgs
        drive_summary_dict["{}_punts".format(col_prepend)] = num_punts
        
            
        return drive_summary_dict
    
    def clean_stats_table_row(self, row, stats_table_dict):
        stat_name_dict = {
            "First Downs" : "first_downs",
            "Rush" : "rush_att",
            "Yds" : "rush_yds",
            "TDs" : "rush_tds",
            "Cmp" : "pass_comp",
            "Att" : "pass_att",
            "Yd" : "pass_yds",
            "TD" : "pass_tds",
            "INT" : "pass_int",
            "Sacked" : "sacks_allowed",
            "Net Pass Yards" : "net_pass_yds",
            "Total Yards" : "total_yds",
            "Fumbles" : "fumbles",
            "Lost" : "fumbles_lost",
            "Turnovers" : "turnovers",
            "Penalties" : "penalties",
            "Yards" : "penalty_yds",
            "Third Down Conv." : "third_down_conv",
            "Fourth Down Conv."  : "fourth_down_conv",
            "Time of Possession" : "time_of_poss"
        }    
        team_id = "{}_stat".format(self.team_table_id)
        opp_id = "{}_stat".format(self.opp_table_id)
        stat = row.th.string
        team_stat = row.find('td', {"data-stat" : team_id}).string
        opp_stat = row.find('td', {"data-stat" : opp_id}).string
        
        if "-" in stat:
            stat_name_split = stat.split("-")
            team_stat_split = team_stat.split("-")
            opp_stat_split = opp_stat.split("-")

            for idx, stat in enumerate(stat_name_split):
                stdized_stat = stat_name_dict[stat]
                team_stat = team_stat_split[idx]
                opp_stat = opp_stat_split[idx]
                stats_table_dict["team_{}".format(stdized_stat)] = team_stat
                stats_table_dict["opp_{}".format(stdized_stat)] = opp_stat
        else:
            stdized_stat = stat_name_dict[stat]        
            stats_table_dict["team_{}".format(stdized_stat)] = team_stat
            stats_table_dict["opp_{}".format(stdized_stat)] = opp_stat

        return stats_table_dict
    
    def get_rush_dir_stats(self):
        game_html = self.game_html_page
        rush_dir_tbl = game_html.find("table", {"id" : "rush_directions"}).tbody
        rush_dir_rows = rush_dir_tbl.findAll("tr")

        team_rush_dir_rows = list(filter(lambda x: self.filter_rush_dir_rows(x, self.team_abbrev), rush_dir_rows))
        opp_rush_dir_rows = list(filter(lambda x: self.filter_rush_dir_rows(x, self.opp_abbrev), rush_dir_rows))

        rush_dirs = ["le", "lt", "lg", "md", "rg", "rt", "re"]
        rush_dir_stats = ["rush", "rush_yds", "rush_td"]

        rush_dir_dict = {}
        for direction in rush_dirs:
            for rush_stat in rush_dir_stats:
                data_stat = "{}_{}".format(rush_stat, direction)
                rush_dir_dict = self.accumulate_rush_dir_stats(rush_dir_dict, team_rush_dir_rows, data_stat, opponent_flg = False)
                rush_dir_dict = self.accumulate_rush_dir_stats(rush_dir_dict, opp_rush_dir_rows, data_stat, opponent_flg = True)
     
        return rush_dir_dict
    
    def accumulate_rush_dir_stats(self, rush_dir_dict, tr_list, data_stat, opponent_flg): 
        vals = [tr.find("td", {"data-stat": data_stat}).string for tr in tr_list]
        vals = [int(val) if val is not None else 0 for val in vals]
        rush_dir_sum = sum(vals)

        dict_key = "opp_{}".format(data_stat) if opponent_flg == True else "team_{}".format(data_stat)
        rush_dir_dict[dict_key] = rush_dir_sum

        return rush_dir_dict

    def filter_rush_dir_rows(self, row, abbrev):
        if row.find("td", {"data-stat" : "team"}) is None:
            val = False
        elif row.find("td", {"data-stat" : "team"}).string == abbrev:
            val = True
        else:
            val = False

        return val
    
    def add_row_to_csv(self, team_row_dict):
        
        data_dir = self.data_dir
        team_file_name = "game_summary_by_team.csv"
        full_path = os.path.join(data_dir, team_file_name)
        if os.path.isfile(full_path):
            team_df = pd.read_csv(full_path)
            team_df = team_df.drop_duplicates()
        else:
            team_df = pd.DataFrame()
        
        for key, val in team_row_dict.items():
            team_row_dict[key] = [val]
        new_row_df =  pd.DataFrame(data=team_row_dict)
        new_row_df_first_cols = ['url', 'team', 'season', 'week', 'opponent', 'line', 'over_under', 'off_pts', 'def_pts_allowed', 'home_flg', 'winner_flg']
        new_row_df_other_cols = [x for x in list(new_row_df.columns) if x not in new_row_df_first_cols]
        new_row_df_cols = new_row_df_first_cols + new_row_df_other_cols
        new_row_df = new_row_df[new_row_df_cols]
        
        team_df = team_df.append(new_row_df, ignore_index = True)
        team_df = team_df.drop_duplicates()
        team_df = team_df[new_row_df_cols]
        team_df.to_csv(full_path, index = False)

        return
    
    def get_game_snap_rows(self, opp_flg):
        
        tbl_id = "{}_snap_counts".format(self.team_table_id) if opp_flg == False else "{}_snap_counts".format(self.opp_table_id)
        team_snaps_tbl = self.game_html_page.find("table", \
            {"id": tbl_id})
        
        if team_snaps_tbl is None:
            team_snaps_rows = []
        else :
            team_snaps_tbl_body = team_snaps_tbl.tbody
            team_snaps_rows = team_snaps_tbl_body.findAll('tr')
        
        return team_snaps_rows
    
    def aggregate_game_stats_by_pos(self, team_players_df, opp_flg, off_snaps, def_snaps):
        col_prepend = "opp" if opp_flg == True else "team"
        pos_stats_dict = {
            "QB" : ["fumbles", "pass_att", "pass_cmp", "pass_int", "pass_sacked", "pass_yds", 
                    "rush_att", "rush_long", "rush_td", "rush_yds", "snaps"],
            "RB" : ["fumbles", "rush_att", "rush_long", "rush_td", "rush_yds",
                    "rec", "rec_long", "rec_td", "rec_yds", "targets", "snaps"],
            "WR" : ["fumbles", "rec", "rec_long", "rec_td", "rec_yds", "targets", "snaps"],
            "TE" : ["fumbles", "rec", "rec_long", "rec_td", "rec_yds", "targets", "snaps"],
            "OL" : [],
            "DL" : ["fumbles_forced", "sacks", "tackles_assists", "tackles_solo", "snaps"],
            "LB" : ["fumbles_forced", "sacks", "tackles_assists", "tackles_solo", "snaps"],
            "DB" : ["def_int", "fumbles_forced", "sacks", "tackles_assists", "tackles_solo", "snaps"],
            "K" : ["fga", "fgm", "xpa", "xpm"],
            "P" : ["punt", "punt_yds_per_punt"]
        }    
        
        pos_player_dict = {}

        for pos in team_players_df["position"].unique():
            pos_colname = pos.lower()
            pos_players_df = team_players_df[team_players_df["position"] == pos].fillna(0)
            pos_stats = pos_stats_dict[pos]
            
            for stat in pos_stats:
                if stat not in pos_players_df.columns.values:
                    continue
                pos_aggregated_stat = pos_players_df[stat].astype(float).sum()
                pos_player_dict["{}_{}_{}_sum".format(col_prepend, pos_colname, stat)] = pos_aggregated_stat

            pos_player_avg_dict = self.get_pos_player_avg_stats(pos_players_df, pos, col_prepend, off_snaps, def_snaps)
            pos_player_dict.update(pos_player_avg_dict)
        
        return pos_player_dict
    
    def get_pos_player_avg_stats(self, pos_players_df, pos, col_prepend, off_snaps, def_snaps):
        
        numerator_key = "numerator"
        denominator_key = "denominator"
        pos_colname = pos.lower()

        avg_stats_def = {
            "yds_per_rec" : {numerator_key : "rec_yds", denominator_key : "rec"},
            "yds_per_rush" : {numerator_key : "rush_yds", denominator_key : "rush_att"},
            "yds_per_target" : {numerator_key: "rec_yds", denominator_key : "targets"},
            "yds_per_snap" : {numerator_key : ["rush_yds", "rec_yds"], denominator_key : None, "denominator_val": off_snaps },
            "yds_per_pass_att" : {numerator_key : "pass_yds", denominator_key : "pass_att"},
            "yds_per_pass_comp" : {numerator_key : "pass_yds", denominator_key : "pass_cmp"},
            "tackles_per_snap" : {numerator_key : ["tackles_assists", "tackles_solo"], denominator_key :  None, "denominator_val": def_snaps},
            "fg_pct" : {numerator_key : "fgm", denominator_key : "fga"}
        }
        pos_stats_dict = {
            "QB" : ["yds_per_pass_att", "yds_per_pass_comp"],
            "RB" : ["yds_per_rush", "yds_per_rec", "yds_per_target", "yds_per_snap"],
            "WR" : ["yds_per_rec", "yds_per_target", "yds_per_snap"],
            "TE" : ["yds_per_rec", "yds_per_target", "yds_per_snap"],
            "OL" : [],
            "DL" : ["tackles_per_snap"],
            "LB" : ["tackles_per_snap"],
            "DB" : ["tackles_per_snap"],
            "P" : [],
            "K" : ["fg_pct"]
        }
        pos_stat_list = pos_stats_dict[pos]

        pos_player_avg_dict = {}
        for stat in pos_stat_list:
            stat_config = avg_stats_def[stat]
            numerator = stat_config[numerator_key]
            denominator = stat_config[denominator_key]

            if denominator is None:
                denominator_val = float(stat_config["denominator_val"])
            elif denominator in pos_players_df.columns.values:
                denominator_val = pos_players_df[denominator].astype(float).sum()
            else:
                denominator_val = 0
                
            if isinstance(numerator, list):
                if all(item in pos_players_df.columns.values for item in numerator):
                    numerator_val = pos_players_df[numerator].astype(float).sum().sum()
                else:
                    numerator_val = 0
            elif numerator in pos_players_df.columns.values:
                numerator_val = pos_players_df[numerator].astype(float).sum()
            else:
                numerator_val = 0

            #denominator_val = pos_players_df[denominator].sum() if denominator is not None else stat_config[]
            if denominator_val == 0:
                avg_stat_val = None
            else:
                avg_stat_val = float(numerator_val) / float(denominator_val)

            pos_player_avg_dict["{}_{}_{}".format(col_prepend, pos_colname, stat)] = avg_stat_val

        return pos_player_avg_dict

    def get_idx_cols(self, games_by_team_df, team_row_dict):
 
        row_key = "row_key"
        df_col_key = "df_col_key"
        idx_col_name = "idx_col_name"
        indices_dict = [
            {row_key: "off_pts", df_col_key: "def_pts_allowed", idx_col_name: "off_pts_idx"},
            {row_key: "def_pts_allowed", df_col_key: "off_pts", idx_col_name: "off_pts_allowed_idx"},
            {row_key: "team_total_yds", df_col_key: "opp_total_yds", idx_col_name: "off_total_yds_idx"},
            {row_key: "opp_total_yds", df_col_key: "team_total_yds", idx_col_name: "total_yds_allowed_idx"},
            {row_key: "team_first_downs", df_col_key: "opp_first_downs", idx_col_name: "off_first_downs_idx"},
            {row_key: "opp_first_downs", df_col_key: "team_first_downs", idx_col_name: "first_downs_allowed_idx"},
            {row_key: "team_rush_yds", df_col_key: "opp_rush_yds", idx_col_name: "off_rush_yds_idx"},
            {row_key: "opp_rush_yds", df_col_key: "team_rush_yds", idx_col_name: "rush_yds_allowed_idx"},
            {row_key: "team_pass_yds", df_col_key: "opp_pass_yds", idx_col_name: "off_pass_yds_idx"},
            {row_key: "opp_pass_yds", df_col_key: "team_pass_yds", idx_col_name: "pass_yds_allowed_idx"},
            {row_key: "opp_sacks_allowed", df_col_key: "team_sacks_allowed", idx_col_name: "sacks_idx"},
            {row_key: "team_sacks_allowed", df_col_key: "opp_sacks_allowed", idx_col_name: "sacks_allowed_idx"},
            {row_key: "team_penalty_yds", df_col_key: "opp_penalty_yds", idx_col_name: "penalty_yds_idx"},
            {row_key: "opp_penalty_yds", df_col_key: "team_penalty_yds", idx_col_name: "opp_penalty_yds_idx"},
            {row_key: "team_turnovers", df_col_key: "opp_turnovers", idx_col_name: "turnovers_idx"},
            {row_key: "opp_turnovers", df_col_key: "team_turnovers", idx_col_name: "turnovers_forced_idx"}
        ]
        
        append_flg = self.append_idx_cols_flg()
        team_idx_dict = {}
        if append_flg == True:
            opp_df = self.get_indiv_team_prevwk_df(games_by_team_df, team_row_dict["opponent"])

            for idx_col in indices_dict:
                col_name = idx_col[idx_col_name]
                row_col_key = idx_col[row_key]
                opp_df_col_key = idx_col[df_col_key]

                team_val = float(team_row_dict[row_col_key])
                opp_df_mean = float(opp_df[opp_df_col_key].mean())

                if opp_df_mean == 0: idx_val = None
                else: idx_val = team_val / opp_df_mean
                team_idx_dict[col_name] = idx_val
        
        return team_idx_dict
        
    def append_idx_cols_flg(self):
        
        append_flg = True
        
        if self.week in ["WildCard", "Division", "ConfChamp", "SuperBowl"]:  
            append_flg = False
        elif self.season == 2012 and int(self.week) <= 3:
            append_flg = False
            
        return append_flg
    
    def get_indiv_team_prevwk_df(self, team_df, team):
        
        season = self.season
        week = self.week 
        num_wks_to_find = self.num_wks_to_find
        week = int(week)
        indiv_team_prevwk_df = pd.DataFrame()
        num_wks_found = 0

#        print("{} / {} / {}".format(team, season, week))
        for prev_wk in range(week - 1, 0, -1):

            #valid_row = get_valid_row(team_df_subset, prev_wk, season)
            team_game_df, num_wks_found = self.append_team_prevwk_game(team_df, team, season, prev_wk, num_wks_found)
            if team_game_df is not None:
                indiv_team_prevwk_df = indiv_team_prevwk_df.append(team_game_df, ignore_index=True)

            if num_wks_found == num_wks_to_find:
                break

        if num_wks_found < num_wks_to_find:
            for prev_wk in range(17, 0, -1):
                team_game_df, num_wks_found = self.append_team_prevwk_game(team_df, team, season - 1, prev_wk, num_wks_found)

                if team_game_df is not None:
                    indiv_team_prevwk_df = indiv_team_prevwk_df.append(team_game_df, ignore_index=True)

                if num_wks_found == num_wks_to_find:
                    break

        return indiv_team_prevwk_df
    
    def append_team_prevwk_game(self, team_df, team, season, prev_wk, num_wks_found):
#        print("  {} / {} / {}".format(team, season, prev_wk))
        
        if team == "Los Angeles Rams":
            teams = ["Los Angeles Rams", "St. Louis Rams"]
        elif team == "Los Angeles Chargers":
            teams = ["Los Angeles Chargers", "San Diego Chargers"]
        else:
            teams = [team]
        team_df_subset = team_df[team_df["week"].astype(str) == str(prev_wk)]
        team_df_subset = team_df_subset[team_df_subset["season"] == season]
        
        valid_row_flg = True if any(team in team_df_subset["team"].unique() for team in teams) else False
        if valid_row_flg == True:
            returned_df = team_df_subset[team_df_subset["team"].isin(teams)]
            num_wks_found += 1
        else:
            returned_df = None

        return returned_df, num_wks_found
    
    def drop_to_csv(self, df, file_name):
        
        data_dir = self.data_dir
        csv_name = "{}.csv".format(file_name)
        full_path = os.path.join(data_dir, csv_name)
        
        if os.path.isfile(full_path):
            team_df = pd.read_csv(full_path)
            team_df = team_df.drop_duplicates()
        else:
            team_df = pd.DataFrame()
        
        team_df = team_df.append(df, ignore_index = True)
        team_df = team_df.drop_duplicates()
        team_df.to_csv(full_path, index = False)
