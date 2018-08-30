import os
import requests
from bs4 import BeautifulSoup
from utils import get_config, get_html

class Season():
    def __init__(self, year, config):
        self.season = year
#         config_dir = os.getcwd().replace('/notebooks', '')
#         config = get_config(config_dir)        
        self.base_url = config['base_url']
        
        self.schedule_url = "{}/years/{}/games.htm".format(self.base_url, self.season)
        self.schedule_games_id = "games"
        self.schedule_page = self.get_season_schedule()
    
    def get_season_schedule(self):
        
        url = self.schedule_url
        schedule_soup = get_html(url)
#         schedule_html = requests.get(url, verify=False).content.decode("utf-8") 
#         schedule_soup = BeautifulSoup(re.sub("<!--|-->","", schedule_html), "lxml")          
        return schedule_soup

    def get_schedule_table(self):
        page = self.schedule_page
        tbl_id = self.schedule_games_id
        schedule_table = page.find(id=tbl_id)
        
        return schedule_table
    
    def get_weekly_dict(self, games_table):
        
        all_trs = games_table.findAll('tr')
        
        game_rows = list(filter(lambda x: x.has_attr('class') == False, all_trs))
        weekly_dict = {}
        
        for game in game_rows:
            week_num = game.find("th", {"data-stat" : "week_num"}).string 

            if week_num in ['Week', None]:
                continue
            if week_num not in weekly_dict.keys():
                weekly_dict[week_num] = [game]
            else:
                weekly_dict[week_num].append(game)
        return weekly_dict