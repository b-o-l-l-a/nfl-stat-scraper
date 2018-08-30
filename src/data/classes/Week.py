
class Week():
    def __init__(self, Season, week, games, upcoming_flg):
        self.season = Season.season       
        self.base_url = Season.base_url
        self.week = week
        self.games = games
        url_week_dict = {
            "WildCard" : 18,
            "Divisional" : 19,
            "ConfChamp" : 20,
            "SuperBowl" : 21
        }
        url_week = url_week_dict[week] if week in url_week_dict.keys() else int(week)
        self.week_url = "{}/years/{}/week_{}.htm".format(self.base_url, self.season, url_week) 