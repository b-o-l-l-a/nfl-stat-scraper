from utils import get_html
import re

class Game():
    def __init__(self, Week, game_summary_row, upcoming_flg):
        
        # set these self variables first so all other fxns in init can run
        self.season = Week.season
        self.week = Week.week
        self.base_url = Week.base_url
        self.upcoming = upcoming_flg

        self.game_url_append = game_summary_row.find("td", {"data-stat":"boxscore_word"}).a["href"]
        self.game_full_url = self.base_url + self.game_url_append        
        self.home_winner_col_name = "home_winner"
        self.game_link_col_name = "game_link"
        self.game_summary_row = game_summary_row
        self.game_summary_cols = game_summary_row.findAll('td')        
        self.game_summary_output_cols = [
            "year",
            "week_num",
            "game_date",
            self.game_link_col_name,
            self.home_winner_col_name, 
            "winner",
            "pts_win",
            "loser",
            "pts_lose"
        ]
        # end
        
        self.game_summary_dict = self.clean_game_summary(game_summary_row)  
        self.teams_list = self.get_teams(game_summary_row)
        self.game_html_page = self.get_game_page()
              
        self.home_team = self.get_home_or_vis(home_flg = True)
        self.vis_team = self.get_home_or_vis(home_flg = False)
        self.favorite = self.get_favorite_or_underdog(favorite_flg = True)
        self.underdog = self.get_favorite_or_underdog(favorite_flg = False)
        self.line = self.get_vegas_stats(stat = "line")
        self.over_under = self.get_vegas_stats(stat = "over_under")
        
    def get_home_or_vis(self, home_flg):
        
        game_summary_dict = self.game_summary_dict
        
        if self.upcoming == False:
            
            winner = game_summary_dict['winner']
            loser = game_summary_dict['loser']
            home_winner = game_summary_dict['home_winner']
            
            if home_flg == True:
                team =  winner if home_winner == True else loser
            else:
                team = loser if home_winner == True else winner 
                
        else:
            team = None
        
        return team
    
    def get_teams(self, game_summary_row):
        
        game_summary_dict = self.game_summary_dict
        teams_list = []
        
        for elem in ["winner", "loser"]:
            team = {
                "team" : game_summary_row.find('td', {'data-stat' : elem}).a.string, 
                "link" : game_summary_row.find('td', {'data-stat' : elem}).a['href']
            }
            
            if elem == "winner" and game_summary_dict['home_winner'] == True:
                team["home_flg"] = True 
            elif elem == "winner" and game_summary_dict['home_winner'] == False:
                team["home_flg"] = False
            elif elem == "loser" and game_summary_dict['home_winner'] == True:
                team["home_flg"] = False
            elif elem == "loser" and game_summary_dict['home_winner'] == False:
                team["home_flg"] = True
            teams_list.append(team)
        
        return teams_list
    
    def get_game_page(self):
        
        game_soup = get_html(self.game_full_url)
        return game_soup
    
    def get_vegas_stats(self, stat):
        
        game_html_page = self.game_html_page
        
        game_info_tbl = game_html_page.find("table", {"id":"game_info"})
        
        if stat == 'line':
            
            vegas_pattern = re.compile(r'Vegas Line')
            line_string = game_html_page.find('th', text=vegas_pattern).parent.td.string
            line_string_split = re.split('([\+-])', line_string)      
            if line_string_split[0] == "Pick":
                return_val = float(0)
            else:
                return_val = float(line_string_split[-1])
            
        elif stat == "over_under":
            vegas_pattern = re.compile(r'Over/Under')
            ou_string = game_html_page.find('th', text=vegas_pattern).parent.td.contents[0]
            return_val = float(ou_string.strip())
            
        return return_val
    
    def get_favorite_or_underdog(self, favorite_flg):
        
        upcoming = self.upcoming
        game_page = self.game_html_page
        teams = [x["team"] for x in self.teams_list]
        game_info_tbl = game_page.find("table", {"id":"game_info"})
        vegas_pattern = re.compile(r'Vegas Line')
        line_string = game_info_tbl.find('th', text=vegas_pattern).parent.td.string
        line_string_split = re.split('([\+-])', line_string)
        if line_string_split[0] == "Pick":
            team = self.home_team if favorite_flg == True else self.vis_team
        else:    
            sign = line_string_split[1]
            if favorite_flg == True and sign == "-":
                team = line_string_split[0].strip()
            elif favorite_flg == True and sign == "+":
                teams.remove(line_string_split[0].strip())
                team = teams[0]
            elif favorite_flg == False and sign == "-":
                teams.remove(line_string_split[0].strip())
                team = teams[0]
            elif favorite_flg == False and sign == "+":
                team = line_string_split[0].strip()
        
        #print(game_info_tbl)
#         if upcoming == False:
#             team = self.game_summary_dict['winner'] if 
        return team
    
    def clean_game_summary(self, game_summary_row):
        
        game_results_cols = self.game_summary_output_cols
        game_summary_cols = game_summary_row.findAll('td')
        
        game_summary_dict = {}
        
        for td in game_summary_cols:
            game_summary_dict = self.clean_game_summary_col(game_summary_dict, td)
        return game_summary_dict
    
    def clean_game_summary_col(self, game_summary_dict, td):
        
        data_stat = td.get('data-stat')
        if data_stat in ["game_date", "pts_lose"]:
            game_summary_dict[data_stat] = td.string
        if data_stat in ["winner", "loser"]:
            game_summary_dict[data_stat] = td.a.string
        if data_stat == "game_location":
            game_summary_dict[self.home_winner_col_name] = False if td.string == "@" else True
        if data_stat == "pts_win":
            game_summary_dict[data_stat] = td.strong.string if td.strong is not None else td.string
            
        return game_summary_dict