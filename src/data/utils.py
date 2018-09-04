import os
from bs4 import BeautifulSoup
import requests
import re
import time
import json
import pandas as pd

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

def dict_to_csv(dict_to_append, path, file_name):

    for key, val in dict_to_append.items():
        dict_to_append[key] = [val]
    
    df_to_append = pd.DataFrame(data=dict_to_append)
    
    csv_name = "{}.csv".format(file_name)
    full_path = os.path.join(path, csv_name)

    if os.path.isfile(full_path):
        df = pd.read_csv(full_path)
        df = df.drop_duplicates()
    else:
        df = pd.DataFrame()

    df = df.append(df_to_append, ignore_index = True)
    df = df.drop_duplicates()
    df.to_csv(full_path, index = False)
    
    return