import os
from bs4 import BeautifulSoup
import requests
import re
import time
import json

def get_config(home_dir):
    path = "{}/config.json".format(home_dir)

    with open(path) as f:
        config = f.readlines()[0]
    
    config_dict = json.loads(config)

    return config_dict

def get_html(url):
    wait_time = 1
    html = requests.get(url).content.decode("utf-8") 
    soup = BeautifulSoup(re.sub("<!--|-->","", html), "lxml")  
    time.sleep(wait_time)
    
    return soup